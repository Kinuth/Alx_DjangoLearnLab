#!/bin/bash

# Exit on error
set -e

echo "--- Installing Dependencies ---"
# Use pip directly to avoid the 'uv' virtualenv error
python3.12 -m pip install -r requirements.txt

echo "--- Collecting Static Files ---"
# REMOVED the 'social_media_api/' prefix because manage.py is in the root
python3.12 manage.py collectstatic --noinput --clear

echo "--- Running Migrations ---"
# REMOVED the 'social_media_api/' prefix
python3.12 manage.py migrate --noinput

echo "--- Build Finished ---"