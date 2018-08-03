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
        "currently": {
            "apparentTemperature": 30.15,
            "cloudCover": 0.42,
            "dewPoint": 18.44,
            "humidity": 0.53,
            "icon": "partly-cloudy-night",
            "ozone": 276.07,
            "precipIntensity": 0,
            "precipProbability": 0,
            "pressure": 1010.66,
            "summary": "Nuages Épars",
            "temperature": 29.11,
            "time": 1530731661,
            "uvIndex": 0,
            "visibility": 16.09,
            "windBearing": 166,
            "windGust": 3.85,
            "windSpeed": 2.11
        },
        "daily": {
            "apparentTemperatureHigh": 35.14,
            "apparentTemperatureHighTime": 1530709200,
            "apparentTemperatureLow": 24.53,
            "apparentTemperatureLowTime": 1530763200,
            "apparentTemperatureMax": 35.14,
            "apparentTemperatureMaxTime": 1530709200,
            "apparentTemperatureMin": 28.12,
            "apparentTemperatureMinTime": 1530691200,
            "cloudCover": 0.53,
            "dewPoint": 19.21,
            "humidity": 0.53,
            "icon": "partly-cloudy-day",
            "moonPhase": 0.69,
            "ozone": 276.42,
            "precipIntensity": 0.094,
            "precipIntensityMax": 0.5055,
            "precipIntensityMaxTime": 1530712800,
            "precipProbability": 0.17,
            "precipType": "rain",
            "pressure": 1010.87,
            "summary": "Nuageux jusque dans la soirée.",
            "sunriseTime": 1530679998,
            "sunsetTime": 1530726111,
            "temperatureHigh": 33.52,
            "temperatureHighTime": 1530709200,
            "temperatureLow": 24.13,
            "temperatureLowTime": 1530763200,
            "temperatureMax": 33.52,
            "temperatureMaxTime": 1530709200,
            "temperatureMin": 26.43,
            "temperatureMinTime": 1530691200,
            "time": 1530658800,
            "uvIndex": 9,
            "uvIndexTime": 1530702000,
            "visibility": 16.09,
            "windBearing": 179,
            "windGust": 6.75,
            "windGustTime": 1530691200,
            "windSpeed": 2.44
        }
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
