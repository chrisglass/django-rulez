#-*- coding: utf-8 -*-
from django.test.testcases import TestCase
from rulez.backends import ObjectPermissionBackend
from rulez import registry
from rulez.exceptions import *

class MockModel():
    pk = 999

    def mock_permission(self, user):
        return True

class MockUser():
    def __init__(self):
        self.pk=666
    def is_anonymous(self):
        return False

class BackendTestCase(TestCase):

    def create_fixtures(self):
        self.user = MockUser()
        self.model = MockModel()
        registry.register('mock_permission', MockModel)

    def test_user_is_tested_for_rule(self):
        self.create_fixtures()
        back = ObjectPermissionBackend()
        res = back.has_perm(self.user, 'mock_permission', self.model)
        self.assertEqual(res, True)
    
    def test_rules_returns_False_for_None_obj(self):
        self.create_fixtures()
        back = ObjectPermissionBackend()
        res = back.has_perm(self.user, 'mock_permission', None)
        self.assertEqual(res, False)

    def test_rules_returns_False_for_inexistant_rule(self):
        self.create_fixtures()
        back = ObjectPermissionBackend()
        res = back.has_perm(self.user, 'whatever_permission', self.model)
        self.assertEqual(res, False)
    
