#!/usr/bin/env python3
from dotenv import load_dotenv, find_dotenv
import os
# Load .env
load_dotenv(find_dotenv())

from api.server import app

app.run(debug=int(os.environ.get('DEBUG', '0')))
