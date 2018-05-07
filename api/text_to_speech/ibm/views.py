import logging
from flask import Blueprint, request, jsonify, Response

from api.exceptions import MissingParameterException, InvalidCredentialsException, \
    BadParameterException, ExternalAPIException, APIException
from api.text_to_speech.ibm.helpers import ibm_send_request
from api.text_to_speech.ibm.constants import LANGUAGES_CODE

tts_ibm = Blueprint('tts_ibm', __name__)
logger = logging.getLogger(__name__)


@tts_ibm.route('/speak', methods=['POST'])
def speak():
    errors = []

    if 'text' not in request.json:
        errors.append(MissingParameterException('text').to_dict())

    if 'language' not in request.json:
        errors.append(MissingParameterException('language').to_dict())

    if errors:
        return jsonify({'errors': errors}), 400

    text = request.json['text']
    language = request.json['language']

    if language not in LANGUAGES_CODE:
        return jsonify({'errors': [BadParameterException('language', valid_values=LANGUAGES_CODE).to_dict()]}), 400

    try:
        res = ibm_send_request(text, language)
    except InvalidCredentialsException as e:
        return jsonify({'errors': [e.to_dict()]}), 401
    except ExternalAPIException as e:
        return jsonify({'errors': [e.to_dict()]}), 503
    except Exception as e:
        logger.error(e)
        return jsonify({'errors': [APIException().to_dict()]}), 500

    return Response(res, mimetype="audio/wav", status=200)
