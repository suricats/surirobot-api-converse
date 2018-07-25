import pytest
import os
import io
from mock import Mock


@pytest.fixture()
def google_request():
    file = os.getcwd() + '/api/speech_to_text/tests/fixtures/audio.wav'
    with io.open(file, 'rb') as audio:
        content = audio.read()
    return {
        'file': content,
        'language': 'fr-FR'
    }


@pytest.fixture()
def corrupted_audio():
    file = os.getcwd() + '/api/speech_to_text/tests/fixtures/corrupted.wav'
    with io.open(file, 'rb') as audio:
        return audio.read()


@pytest.fixture()
def result():
    return {
        'text': 'Bonjour comment tu vas',
        'confidence': 0.9374
    }


@pytest.fixture()
def google_response(result):
    return Mock(results=[Mock(alternatives=[Mock(transcript=result['text'], confidence=result['confidence'])])])
