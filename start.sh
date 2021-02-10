#!/bin/bash

export FLASK_APP=/home/fmoussa/PFE_API/app.py
export FLASK_ENV=development
export ENV_FILE_LOCATION=../.env
python -m flask run --host=0.0.0.0 --port 8080
