import pytest
from mock import patch
from api.exceptions import OperationFailedException
from api.speech_to_text.google.helpers import google_speech_send_request, SpeechClient


# Ensure that STT behaves correctly
@patch.object(SpeechClient, 'recognize', autospec=True)
def test_google_speech_send_request(mock_speech_client, google_request, google_response):
    mock_speech_client.return_value = google_response
    res = google_speech_send_request(google_request['file'], google_request['language'])

    assert mock_speech_client.call_count == 1
    assert google_response.results[0].alternatives[0].transcript == res['text']
    assert google_response.results[0].alternatives[0].confidence == res['confidence']


# Ensure that STT behave correctly when SpeechClient is not working properly
@patch.object(SpeechClient, 'recognize', autospec=True)
def test_google_speech_client_failed(mock_speech_client, google_request, google_response):
    mock_speech_client.side_effect = Exception()
    with pytest.raises(OperationFailedException):
        google_speech_send_request(google_request['file'], google_request['language'])



@pytest.mark.externalapi
def test_service_available(google_request, result):
    res = google_speech_send_request(google_request['file'], google_request['language'])

    assert res['text'] == result['text']
    assert res['confidence'] == result['confidence']
