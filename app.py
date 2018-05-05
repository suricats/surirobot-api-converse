#!/usr/bin/env python3

from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

from speech_to_text import app
app.run(debug=False)
