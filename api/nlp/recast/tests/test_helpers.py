import pytest
import json
from mock import patch, MagicMock, Mock
from api.exceptions import OperationFailedException
from api.nlp.recast.helpers import requests, recast_send_request_dialog, recast_send_request_intent, recast_send_request_memory
from api.nlp.recast.constants import DEFAULT_ID


# Ensure that NLP behaves correctly
@patch.object(requests, 'post', autospec=True)
def test_recast_send_request(mock_post, recast_request, recast_answer_response):
    mock_post.return_value = Mock(status_code=200, json=Mock(return_value=recast_answer_response))
    res = recast_send_request_dialog(recast_request['text'], recast_request['conversation_id'], recast_request['language'])

    assert mock_post.call_count == 1
    assert res['results']['conversation']['id'] == recast_request['conversation_id']
    assert res['results']['conversation']['language'] == recast_request['language']
    assert res['results']['nlp']['source'] == recast_request['text']


# Ensure that NLP behaves correctly when id and language is missing
@patch.object(requests, 'post', autospec=True)
def test_recast_id_and_language_missing(mock_post, recast_request):
    def side_effect(**kwargs):
        assert kwargs.get('data')
        data = json.loads(kwargs['data'])
        assert data.get('conversation_id')
        return Mock(status_code=200, json=Mock(return_value=data['conversation_id']))
    mock_post.side_effect = side_effect
    res = recast_send_request_dialog(text=recast_request['text'])

    assert mock_post.call_count == 1
    assert res == DEFAULT_ID


