import pytest
import json
from mock import patch, MagicMock, Mock
from flask import url_for

from api.exceptions import BadParameterException, MissingParameterException, InvalidCredentialsException, ExternalAPIException, APIException
from api.nlp.recast.helpers import requests, recast_send_request_dialog, recast_send_request_intent, \
    recast_send_request_memory
from api.nlp.recast.constants import DEFAULT_ID, LANGUAGES_CODE, SUPPORTED_FIELDS


# Ensure that NLP behaves correctly when provided correct information
@patch('api.nlp.recast.views.recast_send_request_dialog', autospec=True)
def test_answer_success(mock_recast_send_request_dialog, client, recast_answer_request, recast_answer_response):
    mock_recast_send_request_dialog.return_value = recast_answer_response

    res = client.post(
        url_for('nlp_recast.answer'),
        content_type='application/json',
        data=json.dumps({
            'text': recast_answer_request['text'],
            'language': recast_answer_request['language'],
            'user_id': recast_answer_request['conversation_id'],
        })
    )
    assert res.status_code == 200
    assert mock_recast_send_request_dialog.call_count == 1


# Ensure that NLP behaves correctly when provided bad language
@patch('api.nlp.recast.views.recast_send_request_dialog', autospec=True)
def test_answer_bad_language(mock_recast_send_request_dialog, client, recast_answer_request):
    res = client.post(
        url_for('nlp_recast.answer'),
        content_type='application/json',
        data=json.dumps({
            'text': recast_answer_request['text'],
            'language': 'xx-XX',
            'user_id': recast_answer_request['conversation_id'],
        })
    )
    expected_result = {'errors': [dict(BadParameterException('language', valid_values=LANGUAGES_CODE))]}
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that NLP behaves correctly when language is missing
@patch('api.nlp.recast.views.recast_send_request_dialog', autospec=True)
def test_answer_missing_language(mock_recast_send_request_dialog, client, recast_answer_request, recast_answer_response):
    res = client.post(
        url_for('nlp_recast.answer'),
        content_type='application/json',
        data=json.dumps({
            'text': recast_answer_request['text'],
            'user_id': recast_answer_request['conversation_id'],
        })
    )

    expected_result = {'errors': [dict(MissingParameterException('language'))]}
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that NLP behaves correctly when text is missing
@patch('api.nlp.recast.views.recast_send_request_dialog', autospec=True)
def test_answer_missing_audio_file(mock_recast_send_request_dialog, client, recast_answer_request, recast_answer_response):
    res = client.post(
        url_for('nlp_recast.answer'),
        content_type='application/json',
        data=json.dumps({
            'language': recast_answer_request['language'],
            'user_id': recast_answer_request['conversation_id'],
        })
    )

    expected_result = {'errors': [dict(MissingParameterException('text'))]}
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that NLP behaves correctly when text and language are missing
@patch('api.nlp.recast.views.recast_send_request_dialog', autospec=True)
def test_answer_missing_audio_file_and_language(mock_recast_send_request_dialog, client):
    res = client.post(
        url_for('nlp_recast.answer'),
        content_type='application/json',
        data=json.dumps({"mock": "mock"})
    )

    expected_result = {
        'errors': [
            dict(MissingParameterException('text')),
            dict(MissingParameterException('language'))
        ]
    }
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that NLP behaves correctly when json are empty
@patch('api.nlp.recast.views.recast_send_request_dialog', autospec=True)
def test_answer_empty_json(mock_recast_send_request_dialog, client):
    res = client.post(
        url_for('nlp_recast.answer'),
        content_type='application/json',
        data=json.dumps({})
    )

    expected_result = {
        'errors': [
            dict(APIException('no_content'))
        ]
    }
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that NLP behaves correctly when Recast failed to respond
@patch('api.nlp.recast.views.recast_send_request_dialog', autospec=True)
def test_answer_recast_not_working(mock_recast_send_request_dialog, client, recast_answer_request, recast_answer_response):
    mock_recast_send_request_dialog.side_effect = ExternalAPIException()
    res = client.post(
        url_for('nlp_recast.answer'),
        content_type='application/json',
        data=json.dumps({
            'text': recast_answer_request['text'],
            'language': recast_answer_request['language'],
            'user_id': recast_answer_request['conversation_id'],
        })
    )
    expected_result = {
        'errors': [
            dict(ExternalAPIException())
        ]
    }
    assert res.status_code == 503
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 1


# Ensure that NLP behaves correctly when Recast stopped unexpectedly
@patch('api.nlp.recast.views.recast_send_request_dialog', autospec=True)
def test_answer_recast_stopped(mock_recast_send_request_dialog, client, recast_answer_request):
    mock_recast_send_request_dialog.side_effect = Exception()
    res = client.post(
        url_for('nlp_recast.answer'),
        content_type='application/json',
        data=json.dumps({
            'text': recast_answer_request['text'],
            'language': recast_answer_request['language'],
            'user_id': recast_answer_request['conversation_id'],
        })
    )
    expected_result = {
        'errors': [
            dict(APIException('nlp_answer'))
        ]
    }
    assert res.status_code == 500
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 1


# Ensure that NLP behaves correctly when credentials are invalid
@patch('api.nlp.recast.views.recast_send_request_dialog', autospec=True)
def test_answer_recast_invalid_credentials(mock_recast_send_request_dialog, client, recast_answer_request):
    mock_recast_send_request_dialog.side_effect = InvalidCredentialsException(api_name='Recast')
    res = client.post(
        url_for('nlp_recast.answer'),
        content_type='application/json',
        data=json.dumps({
            'text': recast_answer_request['text'],
            'language': recast_answer_request['language'],
            'user_id': recast_answer_request['conversation_id'],
        })
    )
    expected_result = {
        'errors': [
            dict(InvalidCredentialsException(api_name='Recast'))
        ]
    }
    assert res.status_code == 401
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 1

# INTENT


# Ensure that NLP behaves correctly when provided correct information
@patch('api.nlp.recast.views.recast_send_request_intent', autospec=True)
def test_intent_success(mock_recast_send_request_intent, client, recast_intent_request, recast_intent_response):
    mock_recast_send_request_intent.return_value = recast_intent_response

    res = client.post(
        url_for('nlp_recast.intent'),
        content_type='application/json',
        data=json.dumps({
            'text': recast_intent_request['text'],
            'language': recast_intent_request['language']
        })
    )
    assert mock_recast_send_request_intent.call_count == 1
    assert res.status_code == 200


# Ensure that NLP behaves correctly when provided bad language
@patch('api.nlp.recast.views.recast_send_request_intent', autospec=True)
def test_intent_bad_language(mock_recast_send_request_intent, client, recast_intent_request):
    res = client.post(
        url_for('nlp_recast.intent'),
        content_type='application/json',
        data=json.dumps({
            'text': recast_intent_request['text'],
            'language': 'xx-XX'
        })
    )
    expected_result = {'errors': [dict(BadParameterException('language', valid_values=LANGUAGES_CODE))]}
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_intent.call_count == 0


# Ensure that NLP behaves correctly when text is missing
@patch('api.nlp.recast.views.recast_send_request_intent', autospec=True)
def test_intent_missing_audio_file(mock_recast_send_request_intent, client, recast_intent_request, recast_intent_response):
    res = client.post(
        url_for('nlp_recast.intent'),
        content_type='application/json',
        data=json.dumps({
            'language': recast_intent_request['language']
        })
    )

    expected_result = {'errors': [dict(MissingParameterException('text'))]}
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_intent.call_count == 0



# Ensure that NLP behaves correctly when json are empty
@patch('api.nlp.recast.views.recast_send_request_intent', autospec=True)
def test_intent_empty_json(mock_recast_send_request_intent, client):
    res = client.post(
        url_for('nlp_recast.intent'),
        content_type='application/json',
        data=json.dumps({})
    )

    expected_result = {
        'errors': [
            dict(APIException('no_content'))
        ]
    }
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_intent.call_count == 0


# Ensure that NLP behaves correctly when Recast failed to respond
@patch('api.nlp.recast.views.recast_send_request_intent', autospec=True)
def test_intent_recast_not_working(mock_recast_send_request_intent, client, recast_intent_request, recast_intent_response):
    mock_recast_send_request_intent.side_effect = ExternalAPIException()
    res = client.post(
        url_for('nlp_recast.intent'),
        content_type='application/json',
        data=json.dumps({
            'text': recast_intent_request['text'],
            'language': recast_intent_request['language']
        })
    )
    expected_result = {
        'errors': [
            dict(ExternalAPIException())
        ]
    }
    assert mock_recast_send_request_intent.call_count == 1
    assert res.status_code == 503
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())


# Ensure that NLP behaves correctly when Recast stopped unexpectedly
@patch('api.nlp.recast.views.recast_send_request_intent', autospec=True)
def test_intent_recast_stopped(mock_recast_send_request_intent, client, recast_intent_request):
    mock_recast_send_request_intent.side_effect = Exception()
    res = client.post(
        url_for('nlp_recast.intent'),
        content_type='application/json',
        data=json.dumps({
            'text': recast_intent_request['text'],
            'language': recast_intent_request['language']
        })
    )
    expected_result = {
        'errors': [
            dict(APIException('nlp_intent'))
        ]
    }
    assert res.status_code == 500
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_intent.call_count == 1


# Ensure that NLP behaves correctly when credentials are invalid
@patch('api.nlp.recast.views.recast_send_request_intent', autospec=True)
def test_intent_recast_invalid_credentials(mock_recast_send_request_intent, client, recast_intent_request):
    mock_recast_send_request_intent.side_effect = InvalidCredentialsException(api_name='Recast')
    res = client.post(
        url_for('nlp_recast.intent'),
        content_type='application/json',
        data=json.dumps({
            'text': recast_intent_request['text'],
            'language': recast_intent_request['language']
        })
    )
    expected_result = {
        'errors': [
            dict(InvalidCredentialsException(api_name='Recast'))
        ]
    }
    assert res.status_code == 401
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_intent.call_count == 1
    
# MEMORY


# Ensure that NLP behaves correctly when provided correct information
@patch('api.nlp.recast.views.recast_send_request_memory', autospec=True)
def test_memory_success(mock_recast_send_request_memory, client, recast_memory_request, recast_memory_response):
    mock_recast_send_request_memory.return_value = recast_memory_response

    res = client.post(
        url_for('nlp_recast.memory'),
        content_type='application/json',
        data=json.dumps({
            'field': recast_memory_request['field'],
            'value': recast_memory_request['value'],
            'user_id': recast_memory_request['user_id'],
        })
    )
    assert res.status_code == 200
    assert mock_recast_send_request_memory.call_count == 1


# Ensure that NLP behaves correctly when field is not supported
@patch('api.nlp.recast.views.recast_send_request_memory', autospec=True)
def test_memory_bad_field(mock_recast_send_request_memory, client, recast_memory_request, recast_memory_response):
    mock_recast_send_request_memory.return_value = recast_memory_response

    res = client.post(
        url_for('nlp_recast.memory'),
        content_type='application/json',
        data=json.dumps({
            'field': 'xX-yY-zZ',
            'value': recast_memory_request['value'],
            'user_id': recast_memory_request['user_id'],
        })
    )
    expected_result = {'errors': [dict(BadParameterException('field', valid_values=SUPPORTED_FIELDS))]}
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_memory.call_count == 0


# Ensure that NLP behaves correctly when field is missing
@patch('api.nlp.recast.views.recast_send_request_memory', autospec=True)
def test_memory_missing_field(mock_recast_send_request_memory, client, recast_memory_request, recast_memory_response):
    res = client.post(
        url_for('nlp_recast.memory'),
        content_type='application/json',
        data=json.dumps({
            'value': recast_memory_request['value'],
            'user_id': recast_memory_request['user_id'],
        })
    )

    expected_result = {'errors': [dict(MissingParameterException('field'))]}
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_memory.call_count == 0


# Ensure that NLP behaves correctly when user id is missing
@patch('api.nlp.recast.views.recast_send_request_memory', autospec=True)
def test_memory_missing_audio_file(mock_recast_send_request_memory, client, recast_memory_request, recast_memory_response):
    res = client.post(
        url_for('nlp_recast.memory'),
        content_type='application/json',
        data=json.dumps({
            'field': recast_memory_request['field'],
            'value': recast_memory_request['value']
        })
    )

    expected_result = {'errors': [dict(MissingParameterException('user_id'))]}
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_memory.call_count == 0


# Ensure that NLP behaves correctly when field and user id are missing
@patch('api.nlp.recast.views.recast_send_request_memory', autospec=True)
def test_memory_missing_audio_file_and_language(mock_recast_send_request_memory, client):
    res = client.post(
        url_for('nlp_recast.memory'),
        content_type='application/json',
        data=json.dumps({"mock": "mock"})
    )

    expected_result = {
        'errors': [
            dict(MissingParameterException('field')),
            dict(MissingParameterException('user_id'))
        ]
    }
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_memory.call_count == 0


# Ensure that NLP behaves correctly when json are empty
@patch('api.nlp.recast.views.recast_send_request_memory', autospec=True)
def test_memory_empty_json(mock_recast_send_request_memory, client):
    res = client.post(
        url_for('nlp_recast.memory'),
        content_type='application/json',
        data=json.dumps({})
    )

    expected_result = {
        'errors': [
            dict(APIException('no_content'))
        ]
    }
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_memory.call_count == 0



# Ensure that NLP behaves correctly when Recast failed to respond
@patch('api.nlp.recast.views.recast_send_request_memory', autospec=True)
def test_memory_recast_not_working(mock_recast_send_request_memory, client, recast_memory_request, recast_memory_response):
    mock_recast_send_request_memory.side_effect = ExternalAPIException()
    res = client.post(
        url_for('nlp_recast.memory'),
        content_type='application/json',
        data=json.dumps({
            'field': recast_memory_request['field'],
            'value': recast_memory_request['value'],
            'user_id': recast_memory_request['user_id'],
        })
    )
    expected_result = {
        'errors': [
            dict(ExternalAPIException())
        ]
    }
    assert res.status_code == 503
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_memory.call_count == 1


# Ensure that NLP behaves correctly when Recast stopped unexpectedly
@patch('api.nlp.recast.views.recast_send_request_memory', autospec=True)
def test_memory_recast_stopped(mock_recast_send_request_memory, client, recast_memory_request):
    mock_recast_send_request_memory.side_effect = Exception()
    res = client.post(
        url_for('nlp_recast.memory'),
        content_type='application/json',
        data=json.dumps({
            'field': recast_memory_request['field'],
            'value': recast_memory_request['value'],
            'user_id': recast_memory_request['user_id'],
        })
    )
    expected_result = {
        'errors': [
            dict(APIException('nlp_memory'))
        ]
    }
    assert res.status_code == 500
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_memory.call_count == 1


# Ensure that NLP behaves correctly when credentials are invalid
@patch('api.nlp.recast.views.recast_send_request_memory', autospec=True)
def test_memory_recast_invalid_credentials(mock_recast_send_request_memory, client, recast_memory_request):
    mock_recast_send_request_memory.side_effect = InvalidCredentialsException(api_name='Recast')
    res = client.post(
        url_for('nlp_recast.memory'),
        content_type='application/json',
        data=json.dumps({
            'field': recast_memory_request['field'],
            'value': recast_memory_request['value'],
            'user_id': recast_memory_request['user_id'],
        })
    )
    expected_result = {
        'errors': [
            dict(InvalidCredentialsException(api_name='Recast'))
        ]
    }
    assert res.status_code == 401
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_memory.call_count == 1