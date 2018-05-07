from flask import Flask, redirect, Response
from flask_swagger_ui import get_swaggerui_blueprint
from api.speech_to_text.google.views import stt_google
from api.text_to_speech.ibm.views import tts_ibm

app = Flask(__name__)

app.register_blueprint(stt_google, url_prefix='/api/stt/google')
app.register_blueprint(tts_ibm, url_prefix='/api/tts/ibm')
app.register_blueprint(get_swaggerui_blueprint('/docs', '/docs/openapi.yaml'), url_prefix='/docs')


@app.route('/')
def index():
    return redirect('/docs', code=301)


@app.route('/docs/openapi.yaml')
def swagger_file():
    content = open('./docs/openapi.yaml', 'r')
    return Response(content, mimetype="text/yaml")
