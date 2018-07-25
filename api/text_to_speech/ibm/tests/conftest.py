import pytest


@pytest.fixture()
def ibm_request():
    return {
        'text': "Salut",
        'language': 'fr-FR'
    }