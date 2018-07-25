import io
import json
from google.gax.errors import RetryError
from mock import patch, Mock, MagicMock, mock_open
from flask import url_for

from api.exceptions import BadParameterException, MissingParameterException, OperationFailedException
from api.speech_to_text.google.constants import LANGUAGES_CODE
from api.speech_to_text.google.helpers import SpeechClient



