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
        errors.append(dict(MissingParameterException('audio')))
    if 'language' not in request.form:
        errors.append(dict(MissingParameterException('language')))

    if errors:
        return jsonify({'errors': errors}), 400

    file = request.files['audio']
    file_content = file.read()
    language = request.form['language']
    if language not in LANGUAGES_CODE:
        return jsonify({'errors': [dict(BadParameterException('language', valid_values=LANGUAGES_CODE))]}), 400

    try:
        res = google_speech_send_request(file_content, language)
    except (OperationFailedException, BadParameterException) as e:
        logger.error(e)
        return jsonify({'errors': [dict(e)]}), e.status_code

    return jsonify(res), 200
