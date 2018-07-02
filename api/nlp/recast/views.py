import logging
import json
from flask import Blueprint, request, jsonify, Response

from api.exceptions import MissingParameterException, InvalidCredentialsException, \
    BadParameterException, ExternalAPIException, APIException, MissingHeaderException, BadHeaderException, OperationFailedException

from api.nlp.recast.helpers import recast_send_request_dialog, recast_send_request_intent, recast_send_request_memory
from api.nlp.recast.constants import LANGUAGES_CODE


nlp_recast = Blueprint('nlp_recast', __name__)
logger = logging.getLogger(__name__)


@nlp_recast.route('/answer', methods=['POST'])
def answer():
    errors = []

    if request.json:
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
            res = recast_send_request_dialog(text, request.json.get('id'))
            return jsonify(res['results']), 200
        except InvalidCredentialsException as e:
            return jsonify({'errors': [dict(e)]}), 401
        except ExternalAPIException as e:
            return jsonify({'errors': [dict(e)]}), 503
        except Exception as e:
            logger.error(e)
            return jsonify({'errors': [dict(APIException('converse_parse_nlp'))]}), 500

    else:
        errors.append(dict(APIException('no_content')))
        return jsonify({'errors': errors}), 400


@nlp_recast.route('/intent', methods=['POST'])
def intent():
    errors = []

    if request.json:
        if 'text' not in request.json:
            errors.append(dict(MissingParameterException('text')))

        if errors:
            return jsonify({'errors': errors}), 400

        text = request.json['text']
        language = request.json.get('language')
        if language:
            if language not in LANGUAGES_CODE:
                return jsonify({'errors': [dict(BadParameterException('language', valid_values=LANGUAGES_CODE))]}), 400
        try:
            res = recast_send_request_intent(text, language)
            return jsonify(res['results']), 200
        except InvalidCredentialsException as e:
            return jsonify({'errors': [dict(e)]}), 401
        except ExternalAPIException as e:
            return jsonify({'errors': [dict(e)]}), 503
        except Exception as e:
            logger.error(e)
            return jsonify({'errors': [dict(APIException('converse_parse_nlp'))]}), 500

    else:
        errors.append(dict(APIException('no_content')))
        return jsonify({'errors': errors}), 400



@nlp_recast.route('/memory', methods=['POST'])
def memory():
    pass
