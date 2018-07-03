import os
import requests
import json

from api.exceptions import ExternalAPIException, InvalidCredentialsException, OperationFailedException, ResourceNotFoundException
from .constants import TEST_TEXT, DEFAULT_ID

with open(os.getcwd() + '/res/credentials/recast.json', 'r') as file:
    RECAST_CREDENTIALS = json.load(file)

token = RECAST_CREDENTIALS['token']
headers = {'Authorization': 'Token ' + token, 'Content-Type': 'application/json'}


def recast_send_request_dialog(text, id=None, language=None):
    if not token:
        raise InvalidCredentialsException('recast')
    if id is None:
        id = DEFAULT_ID
    data = {'message': {'content': text, 'type': "text"}, 'conversation_id': id}
    if language:
        data['language'] = language
    data = json.dumps(data)
    res = requests.post(url='https://api.recast.ai/build/v1/dialog', data=data, headers=headers)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 401:
        raise InvalidCredentialsException(api_name='Recast')
    else:
        raise ExternalAPIException(api_name='Recast', description='dialog({})'.format(res.status_code))


def recast_send_request_intent(text, language=None):
    if not token:
        raise InvalidCredentialsException('recast')
    data = {'text': text}
    if language:
        data['language'] = language
    data = json.dumps(data)
    res = requests.post(url='https://api.recast.ai/v2/request', data=data, headers=headers)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 401:
        raise InvalidCredentialsException(api_name='Recast')
    else:
        raise ExternalAPIException(api_name='Recast', description='intent({})'.format(res.status_code))


def recast_send_request_memory(field, user_id, value=None):
    if not token:
        raise InvalidCredentialsException('recast')
    url = 'https://api.recast.ai/build/v1/users/' + RECAST_CREDENTIALS['user_slug'] + '/bots/' + RECAST_CREDENTIALS['bot_slug'] + '/builders/v1/conversation_states/' + user_id
    res = requests.get(url=url, headers=headers)
    if res.status_code == 404:
        # Case: user conversation doesn't exist yet
        recast_send_request_dialog(TEST_TEXT, user_id)
        res = requests.get(url=url, headers=headers)
    if res.status_code == 200:
        memory = res.json()['results']['memory']
        # Case: deleting memory field
        if value is None and memory.get(field) is not None:
            del memory[field]
        # Case: replacing username
        if field == 'username':
            memory['username'] = {
                "fullname": value,
                "raw": value,
                "confidence": 0.99
            }
        # TODO: add others fields here !
        # Update the memory
        data = json.dumps({'memory': memory})
        res1 = requests.put(url=url, data=data, headers=headers)
        if res1.status_code == 200:
            return res1.json()
        elif res.status_code == 401:
            raise InvalidCredentialsException(api_name='Recast')
        else:
            raise ExternalAPIException(api_name='Recast', description='memory_update({})'.format(res1.status_code))
    elif res.status_code == 401:
        raise InvalidCredentialsException(api_name='Recast')
    else:
        raise ExternalAPIException(api_name='Recast', description='memory_get({})'.format(res.status_code))
