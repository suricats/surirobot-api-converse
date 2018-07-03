from flask import Flask, redirect, Response
from flask_swagger_ui import get_swaggerui_blueprint
from api.speech_to_text.google.views import stt_google
from api.text_to_speech.ibm.views import tts_ibm
from api.nlp.recast.views import nlp_recast
from api.converse.views import converse

app = Flask(__name__)

app.register_blueprint(stt_google, url_prefix='/api/stt')
app.register_blueprint(tts_ibm, url_prefix='/api/tts')
app.register_blueprint(nlp_recast, url_prefix='/api/nlp')
app.register_blueprint(converse, url_prefix='/api/converse')
app.register_blueprint(get_swaggerui_blueprint('/docs', '/docs/openapi.yaml'), url_prefix='/docs')


@app.route('/')
def index():
    return redirect('/docs', code=301)


@app.route('/docs/openapi.yaml')
def swagger_file():
    content = open('./docs/openapi.yaml', 'r')
    return Response(content, mimetype="text/yaml")
