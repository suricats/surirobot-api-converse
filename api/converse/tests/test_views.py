import pytest
import json

import requests
from mock import patch, MagicMock, Mock
from flask import url_for
import io
from api.exceptions import BadParameterException, MissingParameterException, InvalidCredentialsException, \
    ExternalAPIException, APIException, BadHeaderException, MissingHeaderException, OperationFailedException
from api.converse.views import get_crypto, get_news, get_weather
from api.converse.constants import AUDIO_FORMATS, SUPPORTED_FORMATS, TEXT_FORMATS, CUSTOM_MESSAGES, DEFAULT_INTENT
from api.converse.views import nlp, tts, stt
from api.speech_to_text.google.constants import LANGUAGES_CODE, SIMPLIFIED_LANGUAGES_CODE


# Ensure that Converse behaves correctly when provided correct information
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
@patch('api.converse.views.check_special_intent', autospec=True)
def test_converse_text_to_text_success(mock_check_special_intent, mock_recast_send_request_dialog, client,
                                       converse_text_request, recast_answer_response):
    mock_recast_send_request_dialog.return_value = recast_answer_response

    mock_check_special_intent.return_value = None
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='application/json',
        data=json.dumps(converse_text_request)
    )
    assert res.status_code == 200
    assert mock_recast_send_request_dialog.call_count == 1
    assert mock_check_special_intent.call_count == 1


# Ensure that Converse behaves correctly when provided correct information
@patch.object(tts, 'ibm_send_request', autospec=True)
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
@patch('api.converse.views.check_special_intent', autospec=True)
def test_converse_text_to_audio_success(mock_check_special_intent, mock_recast_send_request_dialog,
                                        mock_ibm_send_request, client, converse_text_request, converse_audio_response,
                                        recast_answer_response):
    mock_recast_send_request_dialog.return_value = recast_answer_response
    mock_ibm_send_request.return_value = converse_audio_response['body']
    mock_check_special_intent.return_value = None
    res = client.post(
        url_for('converse.conversation-audio'),
        content_type='application/json',
        data=json.dumps(converse_text_request)
    )
    assert res.status_code == 200
    assert mock_recast_send_request_dialog.call_count == 1
    assert mock_check_special_intent.call_count == 1
    assert res.headers.get('JSON')
    assert mock_ibm_send_request.call_count == 1


# Ensure that Converse behaves correctly when provided correct information
@patch.object(stt, 'google_speech_send_request', autospec=True)
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
@patch('api.converse.views.check_special_intent', autospec=True)
def test_converse_audio_to_text_success(mock_check_special_intent, mock_recast_send_request_dialog,
                                        mock_google_speech_send_request, client, converse_audio_request,
                                        converse_text_request, recast_answer_response):
    mock_recast_send_request_dialog.return_value = recast_answer_response
    mock_google_speech_send_request.return_value = {'text': converse_text_request['text'], 'confidence': 0.99}
    mock_check_special_intent.return_value = None
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='multipart/form-data',
        data={
            'audio': (io.BytesIO(converse_audio_request['audio']), 'audio.wav'),
            'language': converse_audio_request['language'],
            'user_id': converse_audio_request['user_id']
        }
    )
    assert res.status_code == 200
    assert mock_recast_send_request_dialog.call_count == 1
    assert mock_check_special_intent.call_count == 1


# Ensure that Converse behaves correctly when provided correct information
@patch.object(tts, 'ibm_send_request', autospec=True)
@patch.object(stt, 'google_speech_send_request', autospec=True)
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
@patch('api.converse.views.check_special_intent', autospec=True)
def test_converse_audio_to_audio_success(mock_check_special_intent, mock_recast_send_request_dialog,
                                         mock_google_speech_send_request, mock_ibm_send_request,
                                         converse_audio_response, client, converse_audio_request,
                                         converse_text_request, recast_answer_response):
    mock_recast_send_request_dialog.return_value = recast_answer_response
    mock_ibm_send_request.return_value = converse_audio_response['body']
    mock_google_speech_send_request.return_value = {'text': converse_text_request['text'], 'confidence': 0.99}
    mock_check_special_intent.return_value = None
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='multipart/form-data',
        data={
            'audio': (io.BytesIO(converse_audio_request['audio']), 'audio.wav'),
            'language': converse_audio_request['language'],
            'user_id': converse_audio_request['user_id']
        }
    )
    assert res.status_code == 200
    assert mock_recast_send_request_dialog.call_count == 1
    assert mock_check_special_intent.call_count == 1


# Ensure that special intents work correctly
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
@patch('api.converse.views.get_weather', autospec=True)
@patch('api.converse.views.get_crypto', autospec=True)
@patch('api.converse.views.get_news', autospec=True)
def test_converse_special_intent_weather(mock_get_news, mock_get_crypto, mock_get_weather,
                                         mock_recast_send_request_dialog, client,
                                         converse_text_request, recast_answer_response, converse_weather_response,
                                         converse_crypto_response, converse_news_response):
    completed_recast_request = recast_answer_response
    completed_recast_request['results']['nlp']['entities'] = {
        "datetime": [
            {
                "formatted": "mercredi 01 août 2018 à 13h07m11s (+0000)",
                "iso": "2018-08-01T13:07:11+00:00",
                "raw": "demain"
            }
        ],
        "location": [
            {
                "formatted": "Paris, France",
                "lat": 48.856614,
                "lng": 2.3522219,
                "raw": "Paris"
            }
        ],
        "cryptomonnaie": [
            {
                "confidence": 0.93,
                "raw": "ethereum",
                "value": "ethereum"
            }
        ]
    }

    # Weather
    completed_recast_request['results']['nlp']['intents'][0]['slug'] = 'get-weather'
    mock_recast_send_request_dialog.return_value = completed_recast_request
    mock_get_weather.return_value = converse_weather_response
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='application/json',
        data=json.dumps(converse_text_request)
    )
    assert res.status_code == 200
    assert mock_get_weather.call_count == 1

    # Crypto
    completed_recast_request['results']['nlp']['intents'][0]['slug'] = 'cryptonews'
    mock_recast_send_request_dialog.return_value = completed_recast_request
    mock_get_crypto.return_value = converse_crypto_response, True
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='application/json',
        data=json.dumps(converse_text_request)
    )
    assert res.status_code == 200
    assert mock_get_crypto.call_count == 1

    # News
    completed_recast_request['results']['nlp']['intents'][0]['slug'] = 'news'
    mock_recast_send_request_dialog.return_value = completed_recast_request
    mock_get_news.return_value = converse_news_response
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='application/json',
        data=json.dumps(converse_text_request)
    )
    assert res.status_code == 200
    assert mock_get_news.call_count == 1

    assert mock_recast_send_request_dialog.call_count == 3


# Ensure that Converse behaves correctly when language is missing
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
def test_converse_missing_language(mock_recast_send_request_dialog, client, converse_text_request,
                                   converse_audio_request):
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='application/json',
        data=json.dumps({
            'text': converse_text_request['text'],
            'user_id': converse_text_request['user_id']
        })
    )
    expected_result = {'errors': [dict(MissingParameterException('language'))]}

    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())

    res = client.post(
        url_for('converse.conversation-audio'),
        content_type='multipart/form-data',
        data={
            'audio': (io.BytesIO(converse_audio_request['audio']), 'audio.wav'),
            'user_id': converse_audio_request['user_id']
        }
    )
    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that Converse behaves correctly when language is not correct
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
def test_converse_bad_language(mock_recast_send_request_dialog, client, converse_text_request, converse_audio_request):
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='application/json',
        data=json.dumps({
            'text': converse_text_request['text'],
            'user_id': converse_text_request['user_id'],
            'language': 'xx-XX'
        })
    )
    expected_result = {'errors': [dict(BadParameterException('language', valid_values=LANGUAGES_CODE))]}
    print(res.data)
    assert res.status_code == 422
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())

    res = client.post(
        url_for('converse.conversation-audio'),
        content_type='multipart/form-data',
        data={
            'audio': (io.BytesIO(converse_audio_request['audio']), 'audio.wav'),
            'language': 'xx-XX',
            'user_id': converse_audio_request['user_id']
        }
    )
    assert res.status_code == 422
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that Converse behaves correctly when text is missing
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
def test_converse_missing_text(mock_recast_send_request_dialog, client, converse_text_request):
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='application/json',
        data=json.dumps({
            'user_id': converse_text_request['user_id'],
            'language': converse_text_request['language']
        })
    )
    expected_result = {'errors': [dict(MissingParameterException('text'))]}

    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that Converse behaves correctly when audio is missing
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
def test_converse_missing_audio(mock_recast_send_request_dialog, client, converse_audio_request):
    res = client.post(
        url_for('converse.conversation-audio'),
        content_type='multipart/form-data',
        data={
            'language': converse_audio_request['language'],
            'user_id': converse_audio_request['user_id']
        }
    )
    expected_result = {'errors': [dict(MissingParameterException('audio'))]}

    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that Converse behaves correctly when header is not correct
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
def test_converse_bad_header(mock_recast_send_request_dialog, client, converse_text_request):
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='xxxxx/xxxx',
        data=json.dumps(converse_text_request)
    )
    expected_result = {'errors': [dict(BadHeaderException('Content-Type', valid_values=SUPPORTED_FORMATS))]}

    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that Converse behaves correctly when header is missing
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
def test_converse_missing_header(mock_recast_send_request_dialog, client, converse_text_request):
    res = client.post(
        url_for('converse.conversation-text'),
        data=json.dumps(converse_text_request)
    )
    expected_result = {'errors': [dict(MissingHeaderException('Content-Type'))]}

    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that Converse behaves correctly when google speech failed
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
@patch.object(stt, 'google_speech_send_request', autospec=True)
def test_converse_stt_fail(mock_google_speech_send_request, mock_recast_send_request_dialog, client, converse_audio_request):
    mock_google_speech_send_request.side_effect = OperationFailedException()
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='multipart/form-data',
        data={
            'audio': (io.BytesIO(converse_audio_request['audio']), 'audio.wav'),
            'language': converse_audio_request['language'],
            'user_id': converse_audio_request['user_id']
        }
    )
    dict_res = json.loads(res.data)
    assert res.status_code == 200
    assert dict_res['message'] == CUSTOM_MESSAGES[SIMPLIFIED_LANGUAGES_CODE[converse_audio_request['language']]]["not-heard"]
    assert dict_res['intent'] == DEFAULT_INTENT
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that Converse behaves correctly when google speech stopped
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
@patch.object(stt, 'google_speech_send_request', autospec=True)
def test_converse_stt_stop(mock_google_speech_send_request, mock_recast_send_request_dialog, client, converse_audio_request):
    mock_google_speech_send_request.side_effect = Exception()
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='multipart/form-data',
        data={
            'audio': (io.BytesIO(converse_audio_request['audio']), 'audio.wav'),
            'language': converse_audio_request['language'],
            'user_id': converse_audio_request['user_id']
        }
    )
    expected_result = {'errors': [dict(ExternalAPIException('Google'))]}

    assert res.status_code == 503
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_recast_send_request_dialog.call_count == 0


# Ensure that Converse behaves correctly when recast credentials are invalid
@patch.object(requests, 'post', autospec=True)
def test_converse_nlp_invalid_credentials(mock_post, client, converse_text_request):
    mock_post.return_value = Mock(status_code=401)
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='application/json',
        data=json.dumps(converse_text_request)
    )
    expected_result = {'errors': [dict(InvalidCredentialsException(api_name='Recast'))]}
    assert res.status_code == 401
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_post.call_count == 1


# Ensure that Converse behaves correctly when services are not working properly
@patch('api.converse.views.check_special_intent', autospec=True)
def test_converse_nlp_services_offline(mock_check_special_intent, client, converse_text_request):
    mock_check_special_intent.side_effect = ExternalAPIException()
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='application/json',
        data=json.dumps(converse_text_request)
    )
    expected_result = {'errors': [dict(ExternalAPIException())]}
    assert res.status_code == 503
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
    assert mock_check_special_intent.call_count == 1


# Ensure that Converse behaves correctly when checking special intents stopped
@patch('api.converse.views.check_special_intent', autospec=True)
def test_converse_nlp_special_intents_stop(mock_check_special_intent, client, converse_text_request):
    mock_check_special_intent.side_effect = Exception()
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='application/json',
        data=json.dumps(converse_text_request)
    )
    assert res.status_code == 500
    assert mock_check_special_intent.call_count == 1

# Ensure that Converse behaves correctly when nlp helper stopped
@patch.object(nlp, 'recast_send_request_dialog', autospec=True)
def test_converse_nlp_stop(mock_recast_send_request_dialog, client, converse_text_request):
    mock_recast_send_request_dialog.side_effect = Exception()
    res = client.post(
        url_for('converse.conversation-text'),
        content_type='application/json',
        data=json.dumps(converse_text_request)
    )
    assert res.status_code == 500
    assert mock_recast_send_request_dialog.call_count == 1