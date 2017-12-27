# Speech To Text API

[![Build Status](https://travis-ci.org/suricats/surirobot-api-speech-to-text.svg?branch=master)](https://travis-ci.org/suricats/surirobot-api-speech-to-text)

The goal of this API is to convert an audio file to text.

## Requirements

* PHP 7.1
* Composer 

## Installation 

* Clone repository and use public folder as webroot
* Install dependencies
  * `composer install`

* Drop your Google API credentials in resources/credentials/surirobot.json or use the suri-downloader:

  * `cp .env.example .env`
  * `nano .env`

* Fill the login & password fields.
* `tools/get-credentials.sh`

* Make storage/ and public/storage/ writeable by your web server.

## API Reference

This project uses API-Speech from Google.

## License

This service uses the Lumen framework
The Lumen framework is open-sourced software licensed under the [MIT 
license](http://opensource.org/licenses/MIT)
