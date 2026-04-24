#!/usr/bin/env python
"""
Simple script to run the Django application
Usage: python run_app.py
"""

import os
import sys
import django
from pathlib import Path
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abc_core.settings')
django.setup()

if __name__ == '__main__':
    # Run server on 0.0.0.0:8000
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
