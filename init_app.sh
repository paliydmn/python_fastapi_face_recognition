#!/bin/sh
apk add python3.10
echo "CHECK PYTHON VERS"
python --version
python init_db.py
pip install -r requirements.txt