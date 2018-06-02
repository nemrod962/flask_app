#!/bin/sh
docker start flask-mongo
cd src/
python main_flask.py
