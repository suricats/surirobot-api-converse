import pytest


@pytest.fixture()
def recast_intent_request():
    return {'text': 'Salut',
            'language': 'fr'}


@pytest.fixture()
def recast_intent_response():
    return {
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
        "sentiment": "vpositive",
        "source": "Bonjour",
    }


@pytest.fixture()
def recast_answer_request():
    return {'text': 'Salut',
            'conversation_id': 'DEFAULT',
            'language': 'fr'}


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
def recast_memory_request():
    return {
        'field': 'username',
        'user_id': 'DEFAULT',
        'value': 'Jean-Mi'
    }


@pytest.fixture()
def recast_memory_response():
    return {
        "results": {
            "builder": {
                "slug": "v1"
            },
            "conversation_id": "DEFAULT",
            "id": "xxxx-xxxx-xxxx-xxxx-xxxxxxxx",
            "language": "fr",
            "memory": {
                "username": {
                    "confidence": 0.99,
                    "fullname": "Jean-Mi",
                    "raw": "Jean-Mi"
                }
            }
        }
    }
