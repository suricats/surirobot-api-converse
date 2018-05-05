import logging
from flask import Blueprint, request, jsonify

from speech_to_text.exceptions import RecognitionFailedException, MissingParameterException, BadParameterException, ExternalAPIException
from speech_to_text.google.helpers import google_speech_send_request

google = Blueprint('google-speech', __name__)
logger = logging.getLogger(__name__)

valid_language_code = [
    'en-US',
    'fr-FR'
]


@google.route('/recognize', methods=['POST'])
def recognize():
    errors = []

    if 'audio_file' not in request.files:
        errors.append(MissingParameterException('audio_file').to_dict())
    if 'language' not in request.form:
        errors.append(MissingParameterException('language').to_dict())

    if errors:
        return jsonify({'errors': errors}), 400

    file = request.files['audio_file']
    language = request.form['language']

    if language not in valid_language_code:
        return jsonify({'errors': [BadParameterException('language', valid_values=valid_language_code).to_dict()]}), 400

    try:
        res = google_speech_send_request(file, language)
    except RecognitionFailedException as e:
        return jsonify({'errors': [e.to_dict()]}), 500
    except Exception as e:
        logger.error(e)
        return jsonify({'errors': [ExternalAPIException('Google').to_dict()]}), 503

    return jsonify(res), 200
