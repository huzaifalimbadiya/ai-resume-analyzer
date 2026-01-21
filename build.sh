#!/usr/bin/env bash
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
