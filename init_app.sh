#!/bin/sh
# apk add python3 --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main
# apk add --no-cache python3
# apk add --no-cache curl jq
# apk add --no-cache python3-dev py3-setuptools
# apk add --no-cache py3-pip
# apk add --no-cache py-pip
# apk add --no-cache build-base g++ make cmake unzip curl-dev
# apk add --no-cache autoconf automake libtool libexecinfo-dev
# apk add --no-cache git
# apk add python3.10
# pip3 install --no-cache --upgrade wheel
# pip3 install --no-cache awscli --upgrade
# pip3 install --no-cache aws-sam-cli --upgrade
# echo "================> CHECK PYTHON VERS: "
# python --version
python3 -m venv env/python
source env/python/bin/activate
pip3 install --upgrade pip
pip3 install wheel
pip3 install -r requirements.txt
python3 init_db.py