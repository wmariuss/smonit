#!/bin/bash

set -e

STAGE=$1

if [ $# -eq 0 ]; then
    echo "Please give an argument to continue the script. Eg. dev or prod."
else
    if [ "$STAGE" == "dev" ]; then
        gunicorn -n smonit smonit.main:app --reload -b 0.0.0.0:8000 --timeout 90 --log-level DEBUG
    elif [ "$STAGE" == "prod" ]; then
        PATH_PID="/run/smonit"
        if [ ! -d "$PATH_PID" ]; then
            mkdir $PATH_PID
        fi
        gunicorn -n smonit smonit.main:app -b 0.0.0.0:8000 --pid $PATH_PID/smonit.pid --timeout 90 --log-level INFO
    fi
fi
