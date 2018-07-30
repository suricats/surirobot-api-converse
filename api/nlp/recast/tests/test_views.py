import pytest
import json
from mock import patch, MagicMock, Mock
from flask import url_for

from api.exceptions import BadParameterException, MissingParameterException, InvalidCredentialsException, ExternalAPIException, APIException
from api.nlp.recast.helpers import requests, recast_send_request_dialog, recast_send_request_intent, \
    recast_send_request_memory
from api.nlp.recast.constants import DEFAULT_ID, LANGUAGES_CODE


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
    print('heee')
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
    print('language')
    expected_result = {'errors': [dict(BadParameterException('language', valid_values=LANGUAGES_CODE))]}
    print(res)
    print(res.data)
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
            'language': recast_answer_request['language'],
            'user_id': recast_answer_request['conversation_id'],
        })
    )

    expected_result = {'errors': [dict(MissingParameterException('language'))]}
    print(res.data)
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that NLP behaves correctly when text is mission
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

    expected_result = {'errors': [dict(MissingParameterException('audio'))]}

    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that NLP behaves correctly when text and language are missing
@patch('api.nlp.recast.views.recast_send_request_dialog', autospec=True)
def test_answer_missing_audio_file_and_language(mock_recast_send_request_dialog, client):
    res = client.post(
        url_for('nlp_recast.answer'),
        content_type='multipart/form-data',
        data=json.dumps({})
    )

    expected_result = {
        'errors': [
            dict(MissingParameterException('audio')),
            dict(MissingParameterException('language'))
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
        content_type='multipart/form-data',
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
