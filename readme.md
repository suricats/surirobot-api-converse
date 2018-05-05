# Speech To Text API

![PyPI - Python Version](https://img.shields.io/badge/python-3.6-blue.svg)

The goal of this API is to convert an audio file to text.

## Requirements

* Python3
* Virtualenvwrapper 

## Installation 

* Clone repository 
* Create virtualenv
  * `mkvirtualenv suri-stt && workon suri-stt`
* Install dependencies
  * `pip install -r requirements.txt`
* Configure .env
  * `cp .env.example .env`

* Option 1 - Drop your Google API credentials in res/credentials.json
* Option 2 (suri-downloader) -  Fill the login & password fields and do:
  * `tools/get-credentials`
  
* Run the server
  * `./app.py`

## API Reference

This project uses Google Cloud Speech.
