#!/bin/bash

# Make migrations
python3 manage.py makemigrations

# Migrate
python3 manage.py migrate

export DJANGO_SETTINGS_MODULE=dvcms.settings

# Create student and lecturer groups
python3 manage.py creategroups

# Create superuser
echo "Please create a super user"
python3 manage.py createsuperuser
