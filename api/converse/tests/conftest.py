import pytest
import io
import os


@pytest.fixture()
def converse_weather_request():
    return {
        "latitude": 12,
        "longitude": 12,
        "time": 1530731661,
        "language": "fr"
    }


@pytest.fixture()
def converse_weather_response():
    return {
        "apparentTemperature": 30.53,
        "cloudCover": 0.42,
        "humidity": 0.52,
        "precipIntensity": 0,
        "precipProbability": 0,
        "summary": "Nuages Épars",
        "temperature": 29.48
    }


@pytest.fixture()
def converse_crypto_request():
    return 'ethereum'


@pytest.fixture()
def converse_crypto_response():
    return {
        "evolution": -3.17,
        "value": 381.972996913
    }


@pytest.fixture()
def converse_news_response():
    return {
        "message": "Affaire Benalla "
    }


@pytest.fixture()
def converse_text_request():
    return {'text': 'Salut',
            'language': 'fr-FR',
            'user_id': 'TEST'}


@pytest.fixture()
def converse_text_response():
    return {
        "input": "Bonjour",
        "intent": "greetings",
        "message": "Bien le bonjour Jean-Mi !",
        "nlp": {
            "message": "Dialog rendered with success",
            "results": {
                "conversation": {
                    "id": "DEFAULT",
                    "language": "fr",
                    "memory": {
                    }
                },
                "messages": [
                    {
                        "content": "Bien le bonjour Jean-Mi !",
                        "type": "text"
                    }
                ],
                "nlp": {
                    "act": "assert",
                    "entities": {},
                    "intents": [
                        {
                            "confidence": 0.99,
                            "description": "Says hello",
                            "slug": "greetings"
                        }
                    ],
                    "language": "fr",
                    "processing_language": "fr",
                    "sentiment": "vpositive",
                    "source": "Bonjour",
                }
            }
        }
    }


@pytest.fixture()
def recast_answer_response():
    return {
        "results": {
            "conversation": {
                "id": "DEFAULT",
                "language": "fr",
                "memory": {},
                "skill": "introduce",
                "skill_occurences": 1
            },
            "messages": [
                {
                    "content": "Salut Jean-Mi !",
                    "type": "text"
                }
            ],
            "nlp": {
                "act": "assert",
                "entities": {},
                "intents": [
                    {
                        "confidence": 0.99,
                        "description": "Says hello",
                        "slug": "greetings"
                    }
                ],
                "language": "fr",
                "processing_language": "fr",
                "sentiment": "vpositive",
                "source": "Salut",
            }
        }

    }


@pytest.fixture()
def converse_audio_request():
    file = os.getcwd() + '/api/speech_to_text/tests/fixtures/audio.wav'
    with io.open(file, 'rb') as audio:
        content = audio.read()
    return {
        'audio': content,
        'language': 'fr-FR',
        'user_id': 'TEST'
    }


@pytest.fixture()
def converse_audio_response():
    file = os.getcwd() + '/api/speech_to_text/tests/fixtures/audio.wav'
    with io.open(file, 'rb') as audio:
        content = audio.read()
    return {
        'body': content,
        'headers': converse_text_response
    }


@pytest.fixture()
def corrupted_audio():
    file = os.getcwd() + '/api/speech_to_text/tests/fixtures/corrupted.wav'
    with io.open(file, 'rb') as audio:
        return audio.read()
