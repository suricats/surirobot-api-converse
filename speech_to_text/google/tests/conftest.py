import pytest
import os
import io
from mock import Mock


@pytest.fixture()
def google_request():
    file = os.getcwd() + '/speech_to_text/tests/fixtures/audio.wav'
    with io.open(file, 'rb') as audio_file:
        content = audio_file.read()
    return {
        'file': content,
        'language': 'fr-FR'
    }


@pytest.fixture()
def result():
    return {
        'text': 'Bonjour comment tu vas',
        'confidence': 0.9374
    }


@pytest.fixture()
def google_response(result):
    return Mock(results=[Mock(alternatives=[Mock(transcript=result['text'], confidence=result['confidence'])])])

