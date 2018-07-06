import logging
import json
import os
import requests
import time as t
from flask import Blueprint, request, jsonify, Response
import timezonefinder
from datetime import datetime
from dateutil import tz

from api.exceptions import MissingParameterException, InvalidCredentialsException, \
    BadParameterException, ExternalAPIException, APIException, MissingHeaderException, BadHeaderException, OperationFailedException

from .constants import AUDIO_FORMATS, TEXT_FORMATS, SUPPORTED_FORMATS, DEFAULT_INTENT, CUSTOM_MESSAGES
from .helpers import get_weather, get_crypto, get_news
from api.speech_to_text.google.constants import LANGUAGES_CODE, SIMPLIFIED_LANGUAGES_CODE

import api.speech_to_text.google.helpers as stt
import api.text_to_speech.ibm.helpers as tts
import api.nlp.recast.helpers as nlp
import dateutil.parser as dp
converse = Blueprint('converse', __name__)
logger = logging.getLogger(__name__)

@converse.route('/text', methods=['POST'], defaults={'want': 'text'})
@converse.route('/audio', methods=['POST'],  defaults={'want': 'audio'})
def conversation(want):
    errors = []
    output = {}
    user_id = None
    type, errors, code = checkRequest(request)
    if errors:
        return jsonify({'errors': errors}), code
    # Case: input is audio
    if type == 'audio':
        if 'user_id' in request.form:
            user_id = request.form['user_id']
        audio = request.files['audio']
        language = request.form['language']
        if language not in LANGUAGES_CODE:
            return jsonify({'errors': [dict(BadParameterException('language', valid_values=LANGUAGES_CODE))]}), 400
        try:
            file_content = audio.read()
        except Exception:
            return jsonify({'errors': [dict(BadParameterException('audio'))]}), 400

        try:
            res = stt.google_speech_send_request(file_content, language)
            text = res["text"]
            stt_confidence = res["confidence"]

            output['input'] = text
            output['stt_confidence'] = stt_confidence
        except OperationFailedException as e:
            logger.error(e)
            api_e = APIException(code='stt_error', msg=str(e))
            return jsonify({'errors': [dict(api_e)]}), api_e.status_code
        except Exception as e:
            logger.error(e)
            return jsonify({'errors': [dict(ExternalAPIException('Google'))]}), 503
    # Case: input is text
    elif type == 'text':
        user_id = request.json.get('user_id')
        text = request.json['text']
        language = request.json['language']

        output['input'] = text
        if language not in LANGUAGES_CODE:
            return jsonify({'errors': [dict(BadParameterException('language', valid_values=LANGUAGES_CODE))]}), 400

    # Analyze the text
    try:
        res_nlp = nlp.recast_send_request_dialog(text, user_id, SIMPLIFIED_LANGUAGES_CODE[language])
        output['nlp'] = res_nlp
        if not res_nlp['results']['messages']:
            message = ""
        else:
            message = res_nlp['results']['messages'][0]['content']
        if not res_nlp['results']['nlp']['intents']:
            intent = DEFAULT_INTENT
            message = CUSTOM_MESSAGES[SIMPLIFIED_LANGUAGES_CODE[language]]["not-understand"]
        else:
            intent = res_nlp['results']['nlp']['intents'][0]['slug']
    except (InvalidCredentialsException, ExternalAPIException) as e:
        return jsonify({'errors': [dict(e)]}), e.status_code
    except Exception as e:
        logger.error(e)
        # msg = "{}: {}".format(e, type(e).__name__)
        api_e = APIException(code='nlp_error', msg=str(e))
        return jsonify({'errors': [dict(api_e)]}), api_e.status_code
    # Check special intents
    try:
        spec_message = checkSpecialIntent(intent, res_nlp['results']['nlp'], SIMPLIFIED_LANGUAGES_CODE[language])
        if spec_message:
            message = spec_message
    except (InvalidCredentialsException, ExternalAPIException) as e:
        return jsonify({'errors': [dict(e)]}), e.status_code
    except Exception as e:
        logger.error(e)
        api_e = APIException(code='services_error', msg=str(e))
        return jsonify({'errors': [dict(api_e)]}), api_e.status_code
    # Regroup informations
    output['message'] = message
    output['intent'] = intent
    # Send the result
    if want == 'text':
        return jsonify(output), 200
    elif want == 'audio':
        try:
            res_tts = tts.ibm_send_request(message, language)
        except (InvalidCredentialsException, ExternalAPIException) as e:
            return jsonify({'errors': [dict(e)]}), e.status_code
        except Exception as e:
            logger.error(e)
            api_e = APIException(code='tts_error', msg=str(e))
            return jsonify({'errors': [dict(api_e)]}), api_e.status_code

        response = Response(res_tts, mimetype="audio/wav", status=200)
        response.headers['JSON'] = jsonify(output)
        return response
    else:
        # Impossible !
        return jsonify({'errors': [dict(APIException(code='invalid_output_format_requested'))]}), 500


def checkSpecialIntent(intent, nlp, language):
    message = None
    # Case: weather
    if intent == "get-weather":
        if nlp['entities'].get('location'):
            latitude = nlp['entities']['location'][0]['lat']
            longitude = nlp['entities']['location'][0]['lng']
            if nlp['entities'].get('datetime'):
                time = dp.parse(nlp['entities']['datetime'][0]['iso']).strftime('%s')
            else:
                time = int(t.time())
            res = get_weather(latitude, longitude, time, language)
            tf = timezonefinder.TimezoneFinder()
            current_tz = tz.gettz(tf.timezone_at(lng=longitude, lat=latitude))
            local_time = datetime.fromtimestamp(time).replace(tzinfo=current_tz)
            if language == 'fr':
                message = 'La météo pour {} le {}: {} avec une temperature de {} °C'.format(nlp['entities']['location'][0]['formatted'], local_time.strftime("%d/%m/%Y à %Hh%M"), res['summary'], res['temperature'])
            else:
                message = 'The weather for {} at {}: {} with a temperature of {} °C'.format(nlp['entities']['location'][0]['formatted'], local_time.strftime("%d/%m/%Y à %Hh%M"), res['summary'], res['temperature'])
        if nlp['entities'].get('cryptomonnaie'):
            crypto = nlp['entities']['cryptomonnaie'][0]['value']
            res = get_crypto(crypto)
            if language == 'fr':
                message = 'La cryptomonnaie {0} vaut actuellement {1:.2f} € et a évolué de {2:.2f} % depuis les dernières 24h'.format(crypto, res['value'], res['evolution'])
            else:
                message = 'The cryptocurrency {0} vaut actuellement {1:.2f} € et a évolué de {2:.2f} % depuis les dernières 24h'.format(crypto, res['value'], res['evolution'])
    if intent == "news":
        res = get_news()
        message = res['message']
    return message


def checkRequest(request):
    errors = []
    content_type = request.headers.get('Content-Type')
    if not content_type:
        return 'none', [dict(MissingHeaderException('Content-Type'))], MissingHeaderException.status_code
    if not content_type.startswith(tuple(SUPPORTED_FORMATS)):
        return 'none', [dict(BadHeaderException('Content-Type', valid_values=SUPPORTED_FORMATS))], BadHeaderException.status_code

    # Case: input is audio
    if content_type.startswith(tuple(AUDIO_FORMATS)):
        if 'audio' not in request.files:
            errors.append(dict(MissingParameterException('audio')))
        if 'language' not in request.form:
            errors.append(dict(MissingParameterException('language')))
        return 'audio', errors, 400 if errors else 200

    # Case: input is text
    elif content_type.startswith(tuple(TEXT_FORMATS)):
        if 'text' not in request.json:
            errors.append(dict(MissingParameterException('text')))

        if 'language' not in request.json:
            errors.append(dict(MissingParameterException('language')))
        return 'text', errors, 400 if errors else 200
    else:
        return 'none', errors, 400
