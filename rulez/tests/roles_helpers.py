#-*- coding: utf-8 -*-
from django.test.testcases import TestCase
from rulez.rolez.cache_helper import get_counter, increment_counter, get_roles
from rulez.rolez.models import ModelRoleMixin
from rulez.rolez.base import AbstractRole

class Mock():
    pk = 999

class MockUser():
    def __init__(self):
        self.pk=666
    def is_anonymous(self):
        return False

# Testing the model inheritence
class Tester(AbstractRole):
    @classmethod
    def is_member(cls, user, obj):
        return getattr(user, 'member', False)
    
class TestModel(ModelRoleMixin):
    pk = 1 # Just to emulate a Django model
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
