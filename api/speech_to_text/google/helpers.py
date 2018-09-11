import os
from google.cloud.speech import SpeechClient, enums, types
from google.gax.errors import RetryError
from api.exceptions import OperationFailedException, BadParameterException

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './res/credentials/google.json'
speech_client = SpeechClient()


def google_speech_send_request(content, language):
    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language
    )
    try:
        response = speech_client.recognize(config, audio)

        return {
            'text': response.results[0].alternatives[0].transcript,
            'confidence': round(float(response.results[0].alternatives[0].confidence), 4)
        }
    except RetryError as e:
        print('{} : {}'.format(type(e).__name__, e))
        raise BadParameterException('audio', ['WAV', '16 bits', 'Mono', '44100Hz', '<1min'])
    except Exception as e:
        raise OperationFailedException from e
