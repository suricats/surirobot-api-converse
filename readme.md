# API Converse

![pipeline status](https://gitlab.kozlek.net/surirobot/api-converse/badges/master/pipeline.svg)
![coverage report](https://gitlab.kozlek.net/surirobot/api-converse/badges/master/coverage.svg)
![PyPI - Python Version](https://img.shields.io/badge/python-3.6-blue.svg)

This API provides all the necessary endpoints to give the `converse` capability to Surirobot. 

## Features

* Speech-to-Text
  * Google Cloud Speech
 
* Text-to-Speech
  * IBM Watson
  
* Natural Language Processing
  * Recast.ai (WIP)

## Requirements

* Python3
* Virtualenvwrapper 

## Installation 

* Clone repository 
* Create virtualenv
```shell
mkvirtualenv api-converse && workon api-converse
```

* Install dependencies
```shell
pip install -r requirements.txt
```

* If you wants to run the test suite:
```shell
pip install -r requirements-dev.txt
```


* Configure .env
```shell
cp .env.example .env
```

* Option 1 - Drop your Google API credentials in res/credentials folder
  * ibm.json - IBM Watson
  * google.json - Google Cloud Speech
 
* Option 2 (suri-downloader) -  Fill the login & password fields in env and do:
```shell
tools/get-credentials
```
  
* Run the server
```shell
./app.py
```

## Docs

The Openapi spec and a postman collection are available in the `doc` folder.
You can render the documentation by pointing your browser at the url given by the server.