import pytest
import requests
from mock import patch, Mock

from api.converse.helpers import get_crypto, get_news, get_weather
from api.exceptions import ExternalAPIException, ResourceNotFoundException


# Ensure that weather helper behaves correctly
@patch.object(requests, 'post', autospec=True)
def test_weather_success(mock_post, converse_weather_request, converse_weather_response):
    mock_post.return_value = Mock(status_code=200, json=Mock(return_value=converse_weather_response))
    get_weather(latitude=converse_weather_request['latitude'], longitude=converse_weather_request['longitude'],
                time=converse_weather_request['time'], language=converse_weather_request['language'])

    assert mock_post.call_count == 1


# Ensure that weather helper behaves correctly when service is offline
@patch.object(requests, 'post', autospec=True)
def test_weather_fail(mock_post, converse_weather_request):
    mock_post.return_value = Mock(status_code=500)
    with pytest.raises(ExternalAPIException):
        get_weather(latitude=converse_weather_request['latitude'], longitude=converse_weather_request['longitude'],
                    time=converse_weather_request['time'], language=converse_weather_request['language'])
    assert mock_post.call_count == 1


# Ensure that crypto helper behaves correctly
@patch.object(requests, 'get', autospec=True)
def test_crypto_success(mock_get, converse_crypto_request, converse_crypto_response):
    mock_get.return_value = Mock(status_code=200, json=Mock(return_value=converse_crypto_response))
    res, found = get_crypto(crypto=converse_crypto_request)
    assert found
    assert mock_get.call_count == 1


# Ensure that crypto helper behaves correctly when service is offline
@patch.object(requests, 'get', autospec=True)
def test_crypto_fail(mock_get, converse_crypto_request):
    mock_get.return_value = Mock(status_code=500)
    with pytest.raises(ExternalAPIException):
        get_crypto(crypto=converse_crypto_request)
    assert mock_get.call_count == 1


# Ensure that crypto helper behaves correctly when resource can't be found
@patch.object(requests, 'get', autospec=True)
def test_crypto_not_found(mock_get):
    mock_get.return_value = Mock(status_code=404)
    res, found = get_crypto(crypto='weird_crypto_name')
    assert not found
    assert mock_get.call_count == 1


# Ensure that news helper behaves correctly
@patch.object(requests, 'get', autospec=True)
def test_news_success(mock_get, converse_news_response):
    mock_get.return_value = Mock(status_code=200, json=Mock(return_value=converse_news_response))
    get_news()

    assert mock_get.call_count == 1


# Ensure that news helper behaves correctly when service is offline
@patch.object(requests, 'get', autospec=True)
def test_news_fail(mock_get):
    mock_get.return_value = Mock(status_code=500)
    with pytest.raises(ExternalAPIException):
        get_news()
    assert mock_get.call_count == 1
