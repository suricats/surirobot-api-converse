from flask import Flask, redirect, Response
from flask_swagger_ui import get_swaggerui_blueprint
from speech_to_text.google.views import google

app = Flask(__name__)

app.register_blueprint(google, url_prefix='/api/google')
app.register_blueprint(get_swaggerui_blueprint('/docs', '/docs/openapi.yaml'), url_prefix='/docs')


@app.route('/')
def index():
    return redirect('/docs', code=301)

@app.route('/docs/openapi.yaml')
def swagger_file():
    content = open('./docs/openapi.yaml')
    return Response(content, mimetype="text/yaml")



