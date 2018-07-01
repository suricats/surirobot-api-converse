import json
from mock import patch, Mock
from flask import url_for

from api.exceptions import BadParameterException, MissingParameterException, InvalidCredentialsException
from api.text_to_speech.ibm.constants import LANGUAGES_CODE
from api.text_to_speech.ibm.helpers import requests


@patch('api.text_to_speech.ibm.views.ibm_send_request', autospec=True)
def test_speak_success(mock_ibm_send_request, client, ibm_request):
    res = client.post(
        url_for('tts_ibm.speak'),
        content_type='application/json',
        data=json.dumps({
            'language': ibm_request['language'],
            'text': ibm_request['text']
        })
    )

    assert mock_ibm_send_request.call_count == 1
    assert res.status_code == 200


@patch('api.text_to_speech.ibm.views.ibm_send_request', autospec=True)
def test_speak_bad_language(mock_ibm_send_request, client, ibm_request):
    res = client.post(
        url_for('tts_ibm.speak'),
        content_type='application/json',
        data=json.dumps({
            'language': 'xx-XX',
            'text': ibm_request['text']
        })
    )

    expected_result = {'errors': [dict(BadParameterException('language', valid_values=LANGUAGES_CODE))]}

    assert mock_ibm_send_request.call_count == 0
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())


@patch('api.text_to_speech.ibm.views.ibm_send_request', autospec=True)
def test_speak_missing_language(mock_ibm_send_request, client, ibm_request):
    res = client.post(
        url_for('tts_ibm.speak'),
        content_type='application/json',
        data=json.dumps({
            'text': ibm_request['text']
        })
    )

    expected_result = {'errors': [dict(MissingParameterException('language'))]}

    assert mock_ibm_send_request.call_count == 0
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())


@patch('api.text_to_speech.ibm.views.ibm_send_request', autospec=True)
def test_speak_missing_text(mock_ibm_send_request, client, ibm_request):
    res = client.post(
        url_for('tts_ibm.speak'),
        content_type='application/json',
        data=json.dumps({
            'language': ibm_request['language'],
        })
    )

    expected_result = {'errors': [dict(MissingParameterException('text'))]}

    assert mock_ibm_send_request.call_count == 0
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())


@patch('api.text_to_speech.ibm.views.ibm_send_request', autospec=True)
def test_speak_missing_text_and_language(mock_ibm_send_request, client):
    res = client.post(
        url_for('tts_ibm.speak'),
        content_type='application/json',
        data=json.dumps({})
    )

    expected_result = {
        'errors': [
            dict(MissingParameterException('text')),
            dict(MissingParameterException('language'))
        ]
    }

    assert mock_ibm_send_request.call_count == 0
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())


@patch.object(requests, 'post', autospec=True)
def test_speak_invalid_credentials(mock_post, client, ibm_request):
    mock_post.return_value = Mock(status_code=401)

    res = client.post(
        url_for('tts_ibm.speak'),
        content_type='application/json',
        data=json.dumps({
            'language': ibm_request['language'],
            'text': ibm_request['text']
        })
    )

    expected_result = {
        'errors': [
            dict(InvalidCredentialsException(api_name='IBM'))
        ]
    }

    assert mock_post.call_count == 1
    assert res.status_code == 401
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
