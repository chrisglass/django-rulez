#-*- coding: utf-8 -*-
from django.test.testcases import TestCase
from rulez.rolez.cache_helper import get_counter, increment_counter, get_roles
from rulez.rolez.models import ModelRoleMixin
from rulez.rolez.base import AbstractRole

class MockModel():
    pk = 999

class MockUser():
    def __init__(self):
        self.pk=666
    def is_anonymous(self):
        return False

