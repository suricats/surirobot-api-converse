import io
import json
from mock import patch

from speech_to_text.exceptions import BadParameterException, MissingParameterException
from speech_to_text.google.constants import LANGUAGES_CODE


@patch('speech_to_text.google.views.google_speech_send_request', autospec=True)
def test_recognize_success(mock_google_speech_send_request, client, google_request, result):
    mock_google_speech_send_request.return_value = result

    res = client.post(
        '/api/google/recognize',
        content_type='multipart/form-data',
        data={
            'language': google_request['language'],
            'audio_file': (io.BytesIO(google_request['file']), 'audio.wav')
        }
    )

    assert res.status_code == 200
    assert json.loads(res.data) == result


@patch('speech_to_text.google.views.google_speech_send_request', autospec=True)
def test_recognize_bad_language(mock_google_speech_send_request, client, google_request, result):
    mock_google_speech_send_request.return_value = result

    res = client.post(
        '/api/google/recognize',
        content_type='multipart/form-data',
        data={
            'language': 'xx-XX',
            'audio_file': (io.BytesIO(google_request['file']), 'audio.wav')
        }
    )

    assert res.status_code == 400
    assert json.loads(res.data) == {'errors': [BadParameterException('language', valid_values=LANGUAGES_CODE).to_dict()]}


@patch('speech_to_text.google.views.google_speech_send_request', autospec=True)
def test_recognize_missing_language(mock_google_speech_send_request, client, google_request, result):
    mock_google_speech_send_request.return_value = result

    res = client.post(
        '/api/google/recognize',
        content_type='multipart/form-data',
        data={
            'audio_file': (io.BytesIO(google_request['file']), 'audio.wav')
        }
    )

    assert res.status_code == 400
    assert json.loads(res.data) == {'errors': [MissingParameterException('language').to_dict()]}


@patch('speech_to_text.google.views.google_speech_send_request', autospec=True)
def test_recognize_missing_audio_file(mock_google_speech_send_request, client, google_request, result):
    mock_google_speech_send_request.return_value = result

    res = client.post(
        '/api/google/recognize',
        content_type='multipart/form-data',
        data={
            'language': google_request['language'],
        }
    )

    assert res.status_code == 400
    assert json.loads(res.data) == {'errors': [MissingParameterException('audio_file').to_dict()]}


@patch('speech_to_text.google.views.google_speech_send_request', autospec=True)
def test_recognize_missing_audio_file_and_language(mock_google_speech_send_request, client, google_request, result):
    mock_google_speech_send_request.return_value = result

    res = client.post(
        '/api/google/recognize',
        content_type='multipart/form-data',
        data={
            'audio_file': google_request['language'],
        }
    )

    expected_result = {
        'errors': [
            MissingParameterException('audio_file').to_dict(),
            MissingParameterException('language').to_dict()
        ]
    }

    assert res.status_code == 400
    assert sorted(json.loads(res.data).items()) == sorted(expected_result.items())
