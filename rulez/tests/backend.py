#-*- coding: utf-8 -*-
from django.test.testcases import TestCase
from rulez import registry
from rulez.backends import ObjectPermissionBackend
from rulez.exceptions import NonexistentFieldName
from rulez.registry import Rule

class MockModel():
    pk = 999

    def __init__(self):
        self.attr_permission = True
        self.attr_wrong_permission = "I'm not a boolean"

    def mock_permission(self, user):
        return True
    
    def mock_simple_permission(self):
        # just a callable, no "user" parameter
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

    def test_user_is_tested_for_rule(self):
        self.create_fixtures()
        registry.register('mock_permission', MockModel)
        back = ObjectPermissionBackend()
        res = back.has_perm(self.user, 'mock_permission', self.model)
        self.assertEqual(res, True)
    
    def test_rules_returns_False_for_None_obj(self):
        self.create_fixtures()
        registry.register('mock_permission', MockModel)
        back = ObjectPermissionBackend()
        res = back.has_perm(self.user, 'mock_permission', None)
        self.assertEqual(res, False)

    def test_rules_returns_False_for_inexistant_rule(self):
        self.create_fixtures()
        registry.register('mock_permission', MockModel)
        back = ObjectPermissionBackend()
        res = back.has_perm(self.user, 'whatever_permission', self.model)
        self.assertEqual(res, False)
    
    def test_user_is_tested_for_simple_rule(self):
        self.create_fixtures()
        registry.register('mock_simple_permission', MockModel)
        back = ObjectPermissionBackend()
        res = back.has_perm(self.user, 'mock_simple_permission', self.model)
        self.assertEqual(res, True)
        
    def test_user_is_tested_for_simple_rule_by_field_name(self):
        self.create_fixtures()
        registry.register('mock_permission', MockModel, field_name='mock_simple_permission')
        back = ObjectPermissionBackend()
        res = back.has_perm(self.user, 'mock_permission', self.model)
        self.assertEqual(res, True)
        
    def test_non_existant_filenames_are_caught(self):
        self.create_fixtures()
        codename = 'mock_permission'
        rule = Rule(codename, MockModel, field_name='I_do_not_exist')
        registry.registry[MockModel].update({codename : rule})
        back = ObjectPermissionBackend()
        
        self.assertRaises(NonexistentFieldName, back.has_perm, self.user, 'mock_permission', self.model)
        
