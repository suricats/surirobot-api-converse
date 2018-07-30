import pytest
import json
from mock import patch, MagicMock, Mock
from api.exceptions import OperationFailedException, InvalidCredentialsException, ExternalAPIException
from api.nlp.recast.helpers import requests, recast_send_request_dialog, recast_send_request_intent, \
    recast_send_request_memory
from api.nlp.recast.constants import DEFAULT_ID


# Ensure that NLP behaves correctly
@patch.object(requests, 'post', autospec=True)
def test_recast_answer_send_request(mock_post, recast_answer_request, recast_answer_response):
    mock_post.return_value = Mock(status_code=200, json=Mock(return_value=recast_answer_response))
    res = recast_send_request_dialog(recast_answer_request['text'], recast_answer_request['conversation_id'],
                                     recast_answer_request['language'])

    assert mock_post.call_count == 1
    assert res['results']['conversation']['id'] == recast_answer_request['conversation_id']
    assert res['results']['conversation']['language'] == recast_answer_request['language']
    assert res['results']['nlp']['source'] == recast_answer_request['text']


# Ensure that NLP behaves correctly when id and language is missing
@patch.object(requests, 'post', autospec=True)
def test_recast_answer_id_and_language_missing(mock_post, recast_answer_request):
    def side_effect(**kwargs):
        assert kwargs.get('data')
        data = json.loads(kwargs['data'])
        assert data.get('conversation_id')
        return Mock(status_code=200, json=Mock(return_value=data['conversation_id']))

    mock_post.side_effect = side_effect
    res = recast_send_request_dialog(text=recast_answer_request['text'])

    assert mock_post.call_count == 1
    assert res == DEFAULT_ID


# Ensure that NLP behaves correctly when credentials are wrong/missing
@patch.object(requests, 'post', autospec=True)
def test_recast_answer_invalid_credentials(mock_post, recast_answer_request):
    mock_post.return_value = Mock(status_code=401)
    with pytest.raises(InvalidCredentialsException):
        recast_send_request_dialog(recast_answer_request['text'], recast_answer_request['conversation_id'],
                                   recast_answer_request['language'])
    assert mock_post.call_count == 1


# Ensure that NLP behaves correctly when Recast is offline
@patch.object(requests, 'post', autospec=True)
def test_recast_answer_recast_offline(mock_post, recast_answer_request):
    mock_post.return_value = Mock(status_code=500)
    with pytest.raises(ExternalAPIException):
        recast_send_request_dialog(recast_answer_request['text'], recast_answer_request['conversation_id'],
                                   recast_answer_request['language'])
    assert mock_post.call_count == 1


# Ensure that NLP behaves correctly when requesting memory update
@patch.object(requests, 'put', autospec=True)
@patch.object(requests, 'get', autospec=True)
def test_recast_memory_send_request(mock_put, mock_get, recast_memory_request, recast_memory_response):
    mock_get.return_value = Mock(status_code=200, json=Mock(return_value=recast_memory_response))
    mock_put.return_value = Mock(status_code=200, json=Mock(return_value=recast_memory_response))
    res = recast_send_request_memory(field=recast_memory_request['field'], user_id=recast_memory_request['user_id'],
                                     value=recast_memory_request['value'])

    assert mock_get.call_count == 1
    assert mock_put.call_count == 1
    assert res['results']['conversation_id'] == recast_memory_request['user_id']
    assert res['results']['memory'][recast_memory_request['field']]


# Ensure that NLP behaves correctly when conversation doesn't exist yet in memory update
@patch('api.nlp.recast.helpers.recast_send_request_dialog', autospec=True)
@patch.object(requests, 'put', autospec=True)
@patch.object(requests, 'get', autospec=True)
def test_recast_memory_conversation_doesnt_exist(mock_get, mock_put, mock_recast_send_request_dialog,
                                                 recast_memory_request, recast_memory_response):
    mock_get.side_effect = [Mock(status_code=404, json=Mock(return_value=recast_memory_response)),
                            Mock(status_code=200, json=Mock(return_value=recast_memory_response))]
    mock_put.return_value = Mock(status_code=200, json=Mock(return_value=recast_memory_response))
    res = recast_send_request_memory(field=recast_memory_request['field'], user_id=recast_memory_request['user_id'],
                                     value=recast_memory_request['value'])

    assert mock_recast_send_request_dialog.call_count == 1
    assert mock_get.call_count == 2
    assert mock_put.call_count == 1
    assert res['results']['conversation_id'] == recast_memory_request['user_id']
    assert res['results']['memory'][recast_memory_request['field']]


# Ensure that NLP behaves correctly when value is empty
@patch.object(requests, 'put', autospec=True)
@patch.object(requests, 'get', autospec=True)
def test_recast_memory_field_is_null(mock_get, mock_put: MagicMock, recast_memory_request, recast_memory_response):
    def side_effect(**kwargs):
        assert kwargs.get('data')
        data = json.loads(kwargs['data'])
        assert data.get('memory') is not None and not data['memory'].get(recast_memory_request['field'])
        return Mock(status_code=200, json=Mock(return_value=recast_memory_response))

    mock_get.return_value = Mock(status_code=200, json=Mock(return_value=recast_memory_response))
    mock_put.side_effect = side_effect
    res = recast_send_request_memory(field=recast_memory_request['field'], user_id=recast_memory_request['user_id'])

    assert mock_get.call_count == 1
    assert mock_put.call_count == 1
    assert res['results']['conversation_id'] == recast_memory_request['user_id']


# Ensure that NLP behaves correctly when credentials are invalids #1
@patch.object(requests, 'put', autospec=True)
@patch.object(requests, 'get', autospec=True)
def test_recast_memory_invalid_credentials_1(mock_get, mock_put: MagicMock, recast_memory_request, recast_memory_response):
    mock_get.return_value = Mock(status_code=200, json=Mock(return_value=recast_memory_response))
    mock_put.return_value = Mock(status_code=401)
    with pytest.raises(InvalidCredentialsException):
        recast_send_request_memory(field=recast_memory_request['field'], user_id=recast_memory_request['user_id'],
                                   value=recast_memory_request['value'])
    assert mock_get.call_count == 1
    assert mock_put.call_count == 1


# Ensure that NLP behaves correctly when credentials are invalids #2
@patch.object(requests, 'put', autospec=True)
@patch.object(requests, 'get', autospec=True)
def test_recast_memory_invalid_credentials_2(mock_get, mock_put: MagicMock, recast_memory_request):
    mock_get.return_value = Mock(status_code=401)
    with pytest.raises(InvalidCredentialsException):
        recast_send_request_memory(field=recast_memory_request['field'], user_id=recast_memory_request['user_id'],
                                   value=recast_memory_request['value'])
    assert mock_get.call_count == 1
    assert mock_put.call_count == 0


# Ensure that NLP behaves correctly when recast is not working properly #1
@patch.object(requests, 'put', autospec=True)
@patch.object(requests, 'get', autospec=True)
def test_recast_memory_recast_offline_1(mock_get, mock_put: MagicMock, recast_memory_request, recast_memory_response):
    mock_get.return_value = Mock(status_code=200, json=Mock(return_value=recast_memory_response))
    mock_put.return_value = Mock(status_code=500)
    with pytest.raises(ExternalAPIException):
        recast_send_request_memory(field=recast_memory_request['field'], user_id=recast_memory_request['user_id'],
                                   value=recast_memory_request['value'])
    assert mock_get.call_count == 1
    assert mock_put.call_count == 1


# Ensure that NLP behaves correctly when recast is not working properly #2
@patch.object(requests, 'put', autospec=True)
@patch.object(requests, 'get', autospec=True)
def test_recast_memory_recast_offline_2(mock_get, mock_put: MagicMock, recast_memory_request):
    mock_get.return_value = Mock(status_code=500)
    with pytest.raises(ExternalAPIException):
        recast_send_request_memory(field=recast_memory_request['field'], user_id=recast_memory_request['user_id'],
                                   value=recast_memory_request['value'])
    assert mock_get.call_count == 1
    assert mock_put.call_count == 0


# Ensure that NLP behaves correctly when requesting intent
@patch.object(requests, 'post', autospec=True)
def test_recast_intent_send_request(mock_post, recast_answer_request, recast_answer_response):
    mock_post.return_value = Mock(status_code=200, json=Mock(return_value=recast_answer_response))
    res = recast_send_request_intent(text=recast_answer_request['text'], language=recast_answer_request['language'])

    assert mock_post.call_count == 1
    assert res['results']['nlp']['source'] == recast_answer_request['text']


# Ensure that NLP behaves correctly when credentials are invalids for intent
@patch.object(requests, 'post', autospec=True)
def test_recast_intent_invalid_credentials(mock_post, recast_answer_request):
    mock_post.return_value = Mock(status_code=401)
    with pytest.raises(InvalidCredentialsException):
        recast_send_request_intent(text=recast_answer_request['text'], language=recast_answer_request['language'])
    assert mock_post.call_count == 1


# Ensure that NLP behaves correctly when credentials are invalids for intent
@patch.object(requests, 'post', autospec=True)
def test_recast_intent_recast_offline(mock_post, recast_answer_request):
    mock_post.return_value = Mock(status_code=500)
    with pytest.raises(ExternalAPIException):
        recast_send_request_intent(text=recast_answer_request['text'], language=recast_answer_request['language'])
    assert mock_post.call_count == 1
