#!/usr/bin/env python
import os

from django.core.management import execute_from_command_line

#Added for test runner
import os, sys
sys.path.insert(0, os.path.abspath('./../../'))


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    execute_from_command_line()
