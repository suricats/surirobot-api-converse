#!/usr/bin/env bash

. $(dirname "$0")/../.env

curl --user ${REMOTE_DATA_LOGIN}:${REMOTE_DATA_PASSWD} https://suri.customer.berdy.pro/credentials/surirobotSTT.json -o resources/credentials/surirobot.json
