AUDIO_FORMATS = [
    'multipart/form-data'
]
TEXT_FORMATS = [
    'application/json'
]
SUPPORTED_FORMATS = AUDIO_FORMATS + TEXT_FORMATS

DEFAULT_INTENT = "no-understand"

CUSTOM_MESSAGES = {
"fr": {
    "not-understand": "Pardonnez-moi, je n'ai pas compris ce que vous avez dit."
},
"en": {
    "not-understand": "Sorry I didn't understand what you said."
}
}
