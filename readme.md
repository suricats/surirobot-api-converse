# API Converse

[![DevBuild Status Dev](https://travis-ci.org/suricats/surirobot-api-converse.svg?branch=dev&label=dev)](https://travis-ci.org/suricats/surirobot-api-converse)
[![Build Status](https://travis-ci.org/suricats/surirobot-api-converse.svg?branch=master)](https://travis-ci.org/suricats/surirobot-api-converse)
[![coverage report](https://codecov.io/gh/suricats/surirobot-api-converse/branch/master/graph/badge.svg)](https://codecov.io/gh/suricats/surirobot-api-converse)
[![PyPI - Python Version](https://img.shields.io/badge/python-3.6-blue.svg)](https://docs.python.org/3/whatsnew/3.6.html)

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
* Virtualenvwrapper ```pip install virtualenvwrapper```
* If you have some trouble with the command ```workon``` see : https://stackoverflow.com/questions/29900090/virtualenv-workon-doesnt-work

## Installation
PYTHON 3.7 NOT SUPPORTED

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


## Configure the environment file
* Configure .env
```shell
cp .env.example .env
```
If you want to use the default environment
- Fill only the ```REMOTE_DATA_LOGIN```  and ```REMOTE_DATA_PASSWD``` fields
- Run the command : ```tools/get-env```

## Configure credentials
* Option 1 - Drop your Google API credentials in res/credentials folder
  * ibm.json - IBM Watson
  * google.json - Google Cloud Speech
 
* Option 2 (suri-downloader) -  Fill the login & password fields in env and do:
```shell
tools/get-credentials
```
  
* Run the dev server 
```shell
./app.py
```

* Run the production server 
```shell
gunicorn -w 4 -b 127.0.0.1:5000 wsgi:app
```

## Docs

The Openapi spec and a postman collection are available in the `doc` folder.
You can render the documentation by pointing your browser at the url given by the server.
