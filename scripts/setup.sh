#!/bin/bash

# Make migrations
python3 manage.py makemigrations

# Migrate
python3 manage.py migrate

# Create student and lecturer groups
python3 manage.py creategroups

# Create superuser
echo "Please create a super user"
python3 manage.py createsuperuser
