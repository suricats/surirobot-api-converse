from google.cloud.speech import SpeechClient, enums, types

from speech_to_text.exceptions import RecognitionFailedException

speech_client = SpeechClient()


def google_speech_send_request(content, language):
    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language
    )

    response = speech_client.recognize(config, audio)

    try:
        return {
            'text': response.results[0].alternatives[0].transcript,
            'confidence': round(float(response.results[0].alternatives[0].confidence), 4)
        }
    except Exception as e:
        raise RecognitionFailedException from e
