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
    "not-understand": "Pardonnez-moi, je n'ai pas compris ce que vous avez dit.",
    "not-heard": "Pardonnez-moi, je n'ai pas entendu ce que vous avez dit.",
    "resource-not-found": "Désolé, je n'arrive pas à trouver l'information demandée.",
    "no-weather": "Désolé, je ne trouve pas la météo pour cette localisation"
},
"en": {
    "not-understand": "Sorry I didn't understand what you said.",
    "not-heard": "Sorry I didn't heard what you said.",
    "resource-not-found": "Sorry, I can't found the information you asked.",
    "no-weather": "Sorry, I can't fouund the weather for this location."
}
}
