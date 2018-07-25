import pytest
import os
import io
from mock import Mock


@pytest.fixture()
def recast_request():
    return {'text': 'Salut',
            'conversation_id': 'DEFAULT',
            'language': 'fr'}


@pytest.fixture()
def recast_memory_request():
    return {
        'field': 'user',
        'user_id': 'DEFAULT',
        'value': 'Jean-Mi'
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
