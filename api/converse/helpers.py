import os
import requests
import json

from api.exceptions import APIException, ExternalAPIException, InvalidCredentialsException, OperationFailedException, ResourceNotFoundException
with open(os.getcwd() + '/res/credentials/recast.json', 'r') as file:
    RECAST_CREDENTIALS = json.load(file)

services_url = os.environ.get('SERVICES_URL')
if services_url is None:
    raise APIException('services_url_not_provided')

headers = {'Content-Type': 'application/json'}


def get_weather(latitude, longitude, time, language):
    data = {'latitude': latitude, 'longitude': longitude, 'time': time, 'language': language}
    data = json.dumps(data)
    res = requests.post(url=services_url+'/api/weather/', data=data, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        raise ExternalAPIException(api_name='API Services - Weather', description='HTTP code: {}\nDetails: {}'.format(res.status_code, res.content))


def get_crypto(crypto):
    res = requests.get(url=services_url+'/api/crypto/'+crypto, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        raise ExternalAPIException(api_name='API Services - Cryptonews', description='HTTP code: {}\nDetails: {}'.format(res.status_code, res.content))


def get_news():
    res = requests.get(url=services_url+'/api/news', headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        raise ExternalAPIException(api_name='API Services - Cryptonews', description='HTTP code: {}\nDetails: {}'.format(res.status_code, res.content))
