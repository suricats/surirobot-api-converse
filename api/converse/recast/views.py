import logging
from flask import Blueprint, request, jsonify, Response

from api.exceptions import MissingParameterException, InvalidCredentialsException, \
    BadParameterException, ExternalAPIException, APIException

tts_ibm = Blueprint('converse_recast', __name__)
logger = logging.getLogger(__name__)


@tts_ibm.route('/nlp', methods=['GET'])
def speak():
    errors = []

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
