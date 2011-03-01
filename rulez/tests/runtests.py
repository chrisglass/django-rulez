#!/usr/bin/env python

import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
parent = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))))

sys.path.insert(0, parent)

from django.test.simple import run_tests

def runtests():
    failures = run_tests([
        'rulez.BackendTest',
#        'django_rules.RulePermissionTest',
        'rulez.UtilsTest',
        ], verbosity=1, interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    runtests()

