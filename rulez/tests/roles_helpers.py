#-*- coding: utf-8 -*-
from django.test.testcases import TestCase
from rulez.roles.cache_helper import get_counter, increment_counter, get_roles
from rulez.roles.models import ModelRoleMixin
from rulez.roles.roles import AbstractRole

class Mock():
    id = 999

class MockUser():
    id = 666

# Testing the model inheritence
class Tester(AbstractRole):
    
    def is_member(self,user, obj):
        return getattr(user, 'member', False)
    
class TestModel(ModelRoleMixin):
    id = 1 # Just to emulate a Django model
    roles = [Tester]

# The actual test case
class RolesCacheHelperTestCase(TestCase):
    
    def test_incrementing_counter_works(self):
        obj = Mock()
        first = get_counter(obj)
        self.assertEqual(first, 0)
        increment_counter(obj)
        second = get_counter(obj)
        self.assertNotEqual(second, first)
        
    def test_get_empty_roles_works(self):
        model = TestModel()
        user = MockUser()
        res = get_roles(user, model)
        self.assertEqual(res, [])
        
    def test_user_with_role_works(self):
        # Now let's make the user a member!
        model = TestModel()
        user = MockUser()
        setattr(user, 'member', True)
        res = get_roles(user, model)
        self.assertEqual(len(res), 1)
        
    def test_has_role_works(self):
        model = TestModel()
        user = MockUser()
        setattr(user, 'member', True)
        res = model.has_role(user, Tester)
        self.assertEqual(res, True)
        
    def test_doesnt_have_role_works(self):
        model = TestModel()
        user = MockUser()
        res = model.has_role(user, Tester)
        self.assertEqual(res, False)