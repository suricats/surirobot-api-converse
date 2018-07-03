import logging
from flask import request, jsonify, Blueprint

from api.exceptions import OperationFailedException, MissingParameterException, \
    BadParameterException, ExternalAPIException
from api.speech_to_text.google.helpers import google_speech_send_request
from api.speech_to_text.google.constants import LANGUAGES_CODE


stt_google = Blueprint('stt_google', __name__)
logger = logging.getLogger(__name__)


@stt_google.route('/recognize', methods=['POST'])
def recognize():
    errors = []

    if 'audio' not in request.files:
        errors.append(dict(MissingParameterException('audio_file')))
    if 'language' not in request.form:
        errors.append(dict(MissingParameterException('language')))

    if errors:
        return jsonify({'errors': errors}), 400

    file = request.files['audio']
    language = request.form['language']

    if language not in LANGUAGES_CODE:
        return jsonify({'errors': [dict(BadParameterException('language', valid_values=LANGUAGES_CODE))]}), 400

    try:
        file_content = file.read()
    except Exception:
        return jsonify({'errors': [dict(BadParameterException('audio_file'))]}), 400

    try:
        res = google_speech_send_request(file_content, language)
    except OperationFailedException as e:
        return jsonify({'errors': [dict(e)]}), 500
    except Exception as e:
        logger.error(e)
        return jsonify({'errors': [dict(ExternalAPIException('Google'))]}), 503

    return jsonify(res), 200
