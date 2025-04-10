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
# python -m venv env/python
# source env/python/bin/activate
# apk add libgl1-mesa-dev
# pip install --upgrade pip
# pip install wheel
# pip install -r requirements.txt
# python init_db.py

#!/bin/sh
# Install required packages
apt-get update
apt-get install -y python3 python3-dev python3-venv python3-pip build-essential \
    curl jq git libgl1-mesa-dev cmake

# Create and activate a virtual environment
# python3 -m venv env/python
# source env/python/bin/activate

# Upgrade pip and setuptools
pip install --upgrade pip setuptools

# Install dependencies
pip install wheel
pip install -r requirements.txt
echo "================> CHECK PYTHON VERS: "
pip list
# Initialize the database
echo "Starting database initialization..."
#python app/init_db.py
python -m app.init_db
echo "Database initialization completed."