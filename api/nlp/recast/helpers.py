import os
import requests
import json

from api.exceptions import ExternalAPIException, InvalidCredentialsException, OperationFailedException
token = os.environ.get('RECAST_DEV_TOKEN', '')
headers = {'Authorization': 'Token ' + token, 'Content-Type': 'application/json'}


def recast_send_request_dialog(text, id=None):
    if not token:
        raise InvalidCredentialsException('recast')
    if not id:
        id = "DEFAULT"
    data = json.dumps(
    {'message': {
        'content': text,
        'type': "text"
        },
    'conversation_id': id})
    res = requests.post(url='https://api.recast.ai/build/v1/dialog', data=data, headers=headers)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 401:
        raise InvalidCredentialsException(api_name='Recast')
    else:
        raise ExternalAPIException(api_name='Recast')


def recast_send_request_intent(text, language):
    if not token:
        raise InvalidCredentialsException('recast')
    data = json.dumps({'text': text, 'language': language})
    res = requests.post(url='https://api.recast.ai/v2/request', data=data, headers=headers)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 401:
        raise InvalidCredentialsException(api_name='Recast')
    else:
        raise ExternalAPIException(api_name='Recast')


def recast_send_request_memory(field, value, user_id):
    if not token:
        raise InvalidCredentialsException('recast')
    # IN PROGRESS
    res = {}
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 401:
        raise InvalidCredentialsException(api_name='Recast')
    else:
        raise ExternalAPIException(api_name='Recast')
