#!/bin/bash

set -e

gunicorn --reload -b 0.0.0.0:8000 smonit.main:app --timeout 90 --log-level info
