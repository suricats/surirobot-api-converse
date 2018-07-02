#!/usr/bin/env python3
from dotenv import load_dotenv, find_dotenv
# Load .env
load_dotenv(find_dotenv())

from api.server import app

app.run(debug=False)
