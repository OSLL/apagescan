#!/usr/bin/env bash
python3 -m virtualenv .venv
source .venv/bin/activate
python3 -m pip install -r ./requirements.txt
pyinstaller --onefile --noconsole main.py
cp dist/main apagescan