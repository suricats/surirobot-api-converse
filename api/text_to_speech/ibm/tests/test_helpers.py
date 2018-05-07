import pytest

from api.text_to_speech.ibm.helpers import ibm_send_request


@pytest.mark.externalapi
def test_service_available(ibm_request):
    res = ibm_send_request(ibm_request['text'], ibm_request['language'])
    assert type(res) == bytes
