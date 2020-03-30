#!/bin/bash
while ! nc -z db 3306; do echo "DB not up. Waiting..."; sleep 5; done
python3 -u main.py
