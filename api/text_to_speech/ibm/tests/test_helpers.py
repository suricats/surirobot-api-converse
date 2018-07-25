import pytest
from mock import patch, Mock

from api.text_to_speech.ibm.helpers import ibm_send_request
from api.text_to_speech.ibm.helpers import requests


@pytest.mark.externalapi
def test_service_available(ibm_request):
    res = ibm_send_request(ibm_request['text'], ibm_request['language'])
    assert type(res) == bytes


# Ensure that TTS send information
@patch.object(requests, 'post', autospec=True)
def test_helper_available(mock_post, ibm_request):
    mock_post.return_value = Mock(status_code=200, content='mock')
    res = ibm_send_request(ibm_request['text'], ibm_request['language'])

    assert res == 'mock'
    assert mock_post.call_count == 1