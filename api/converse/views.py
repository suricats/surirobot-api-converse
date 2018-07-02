import logging
from flask import Blueprint, request, jsonify, Response

from api.exceptions import MissingParameterException, InvalidCredentialsException, \
    BadParameterException, ExternalAPIException, APIException, MissingHeaderException, BadHeaderException, OperationFailedException

from api.speech_to_text.google.constants import LANGUAGES_CODE
from api.converse.constants import AUDIO_FORMATS, TEXT_FORMATS, SUPPORTED_FORMATS
import api.speech_to_text.google.helpers as stt
import api.text_to_speech.ibm.helpers as tts
import api.nlp.recast.helpers as nlp
converse = Blueprint('converse', __name__)
logger = logging.getLogger(__name__)


@converse.route('/text', methods=['POST'], defaults={'want': 'text'})
@converse.route('/audio', methods=['POST'],  defaults={'want': 'audio'})
def conversation(want):
    print(want)
    errors = []
    user_id = None
    type, errors, code = checkRequest(request)
    if errors:
        return jsonify({'errors': errors}), code

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
            return jsonify({'errors': [dict(BadParameterException('audio_file'))]}), 400

        try:
            res = stt.google_speech_send_request(file_content, language)
            text = res["text"]
            stt_confidence = res["confidence"]

        except OperationFailedException as e:
            return jsonify({'errors': [dict(APIException(code='stt_error', msg=str(e)))]}), 500
        except Exception as e:
            logger.error(e)
            return jsonify({'errors': [dict(ExternalAPIException('Google'))]}), 503
    # Case: input is text
    elif type == 'text':
        if 'user_id' in request.json:
            user_id = request.json['user_id']
        text = request.json['text']
        language = request.json['language']
        if language not in LANGUAGES_CODE:
            return jsonify({'errors': [dict(BadParameterException('language', valid_values=LANGUAGES_CODE))]}), 400

    # NLP
    res_nlp = nlp.recast_send_request_dialog(text, user_id)
    message = res_nlp['results']['messages'][0]['content']
    intent = res_nlp['results']['nlp']['intents'][0]['slug']
    return jsonify({'message': message, 'intent': intent}), 200


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
            errors.append(dict(MissingParameterException('audio_file')))
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
