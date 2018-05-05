from flask import Flask
from speech_to_text.google.views import google

app = Flask(__name__)

app.register_blueprint(google, url_prefix='/api/google')
