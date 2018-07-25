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
        errors.append(dict(MissingParameterException('text')))

    if 'language' not in request.json:
        errors.append(dict(MissingParameterException('language')))

    if errors:
        return jsonify({'errors': errors}), 400

    text = request.json['text']
    language = request.json['language']

    if language not in LANGUAGES_CODE:
        return jsonify({'errors': [dict(BadParameterException('language', valid_values=LANGUAGES_CODE))]}), 400

    try:
        res = ibm_send_request(text, language)
    except (InvalidCredentialsException, ExternalAPIException) as e:
        return jsonify({'errors': [dict(e)]}), e.status_code
    except Exception as e:
        logger.error(e)
        api_e = APIException()
        return jsonify({'errors': [dict(api_e)]}), api_e.status_code

    return Response(res, mimetype="audio/wav", status=200)
