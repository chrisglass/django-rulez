#-*- coding: utf-8 -*-
from django.test.testcases import TestCase
from rulez import registry
from rulez.exceptions import NonexistentFieldName

class MockModel():
    pk = 999

    def mock_permission(self):
        return True

class MockUser():
    def __init__(self):
        self.pk=666
    def is_anonymous(self):
        return False

class RegistryTestCase(TestCase):
    def test_rule_is_registered(self):
        registry.register('mock_permission', MockModel)
        # if it's been registered properly we should be able to get() something
        res = registry.get('mock_permission', MockModel)
        self.assertNotEqual(res, None)
        self.assertNotEqual(res, {})
         
    def test_registration_raises_non_existant_field_names(self):
        self.assertRaises(NonexistentFieldName, registry.register, 
            'mock_permission', MockModel, field_name='inexistant'
        )
         
