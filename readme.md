# Speech To Text API

![Build status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![PyPI - Python Version](https://img.shields.io/badge/python-3.6-blue.svg)
![Codecov](https://img.shields.io/badge/coverage-85%25-green.svg)

The goal of this API is to convert an audio file to text.

## Requirements

* Python3
* Virtualenvwrapper 

## Installation 

* Clone repository 
* Create virtualenv
```shell
mkvirtualenv suri-stt && workon suri-stt
```

* Install dependencies
```shell
pip install -r requirements.txt
```

* Configure .env
```shell
cp .env.example .env
``

* Option 1 - Drop your Google API credentials in res/credentials.json
* Option 2 (suri-downloader) -  Fill the login & password fields and do:
```shell
tools/get-credentials
```
  
* Run the server
```shell
./app.py
```

## API Reference

This project uses Google Cloud Speech.
