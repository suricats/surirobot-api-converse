import requests
import os
import json

from api.exceptions import ExternalAPIException, InvalidCredentialsException
from api.text_to_speech.ibm.constants import LANGUAGES_CODE_MAPPING as LANG_MAP, DEFAULT_LANGUAGE

with open(os.getcwd() + '/res/credentials/ibm.json', 'r') as file:
    IBM_CREDENTIALS = json.load(file)


def ibm_send_request(text, language):
    url = IBM_CREDENTIALS['url'] + '/v1/synthesize?voice={}'.format(LANG_MAP.get(language, DEFAULT_LANGUAGE))
    data = json.dumps({
        'text': text
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'audio/wav'
    }
    auth = (IBM_CREDENTIALS['username'], IBM_CREDENTIALS['password'])

    res = requests.post(url=url, data=data, headers=headers, auth=auth)

    if res.status_code == 200:
        return res.content
    elif res.status_code == 401:
        raise InvalidCredentialsException(api_name='IBM')
    else:
        raise ExternalAPIException(api_name='IBM')
