import logging
from flask import Blueprint, request, jsonify

from speech_to_text.exceptions import RecognitionFailedException
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
        errors.append('Missing audio_file parameter.')
    if 'language' not in request.form:
        errors.append('Missing language parameter.')

    if errors:
        return jsonify({'errors': errors}), 400

    file = request.files['audio_file']
    language = request.form['language']

    if language not in valid_language_code:
        return jsonify({'errors': ['Bad language code. Valid code are {}'.format(', '.join(valid_language_code))]}), 400

    try:
        res = google_speech_send_request(file, language)
    except RecognitionFailedException as e:
        return jsonify({'errors': [str(e)]}), 503
    except Exception as e:
        logger.error(e)
        return jsonify({'errors': ['Google API is unreliable.']}), 503

    return jsonify(res), 200
