import logging
from flask import Blueprint, request, jsonify, Response

from api.exceptions import MissingParameterException, InvalidCredentialsException, \
    BadParameterException, ExternalAPIException, APIException, MissingHeaderException, BadHeaderException, OperationFailedException

from api.speech_to_text.google.constants import LANGUAGES_CODE
import api.speech_to_text.google.helpers as stt
import api.text_to_speech.ibm.helpers as tts

converse_recast = Blueprint('converse_recast', __name__)
logger = logging.getLogger(__name__)


AUDIO_FORMATS = [
    'multipart/form-data'
]
TEXT_FORMATS = [
    'application/json'
]
SUPPORTED_FORMATS = AUDIO_FORMATS + TEXT_FORMATS


@converse_recast.route('/text', methods=['POST'])
def get_text():
    errors = []
    if request.json:
        if 'text' not in request.json:
            errors.append(dict(MissingParameterException('text')))

        if 'language' not in request.json:
            errors.append(dict(MissingParameterException('language')))

        if errors:
            return jsonify({'errors': errors}), 400

        try:
            res = "Hi"
        except InvalidCredentialsException as e:
            return jsonify({'errors': [dict(e)]}), 401
        except ExternalAPIException as e:
            return jsonify({'errors': [dict(e)]}), 503
        except Exception as e:
            logger.error(e)
            return jsonify({'errors': [dict(APIException())]}), 500

        return Response(res, mimetype="audio/wav", status=200)
    else:
        errors.append(dict(APIException('no_content')))
        return jsonify({'errors': errors}), 400


@converse_recast.route('/audio', methods=['POST'])
def get_audio():
    errors = []
    type, errors, code = checkRequest(request)
    if errors:
        return jsonify({'errors': errors}), code

    if type == 'audio':
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
            return jsonify(text), 200
        except OperationFailedException as e:
            return jsonify({'errors': [dict(APIException(code='stt_error', msg=str(e)))]}), 500
        except Exception as e:
            logger.error(e)
            return jsonify({'errors': [dict(ExternalAPIException('Google'))]}), 503
    # Case: input is text
    elif type == 'text':
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

        return jsonify(request.json["text"]), 200


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
