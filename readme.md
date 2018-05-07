# API Converse

![Build status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![PyPI - Python Version](https://img.shields.io/badge/python-3.6-blue.svg)
![Codecov](https://img.shields.io/badge/coverage-88%25-green.svg)

This API provides all the necessary endpoints to give the `converse` capability to Surirobot. 

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