#-*- coding: utf-8 -*-
from __future__ import with_statement
from django.contrib.auth.models import AnonymousUser, User
from django.core import cache
from django.test.testcases import TestCase
from rulez.exceptions import RulesException
from rulez.rolez.base import AbstractRole
from rulez.rolez.cache_helper import get_counter, increment_counter, get_roles, \
    get_user_pk, roles_key
from rulez.rolez.models import ModelRoleMixin

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
    
    def setUp(self):
        cache.cache.clear()
    
    def test_incrementing_counter_works(self):
        obj = Mock()
        first = get_counter(obj)
        self.assertEqual(first, 0)
        increment_counter(obj)
        second = get_counter(obj)
        self.assertNotEqual(second, first)
        
    def test_incrementing_counter_works_for_none(self):
        increment_counter(None)
        
    def test_get_roles_for_None_raises(self):
        with self.assertRaises(AttributeError):
            res = get_counter(None)
            self.assertEqual(res, None)
        
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
        
    def test_get_roles_cache_works(self):
        # Now let's assert the cache works.
        model = TestModel()
        user = MockUser()
        setattr(user, 'member', True)
        res = get_roles(user, model)
        self.assertEqual(len(res), 1)
        res2 = get_roles(user, model)
        self.assertEqual(len(res2), 1)
        self.assertEqual(res, res2)
        
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
        
    def test_get_anonymous_user_works(self):
        anon = AnonymousUser()
        res = get_user_pk(anon)
        self.assertEqual(res, 'anonymous')
        
    def test_get_roles_works_for_anonymous(self):
        model = TestModel()
        user = AnonymousUser()
        res = model.has_role(user, Tester)
        self.assertEqual(res, False)
    
    def test_get_counter_does_not_return_spaces(self):
        obj = Mock()
        user = MockUser()
        roles_key(user, obj) # The first time, the counter == 0
        increment_counter(obj) # Now there should be a timestamp
        res = roles_key(user, obj)
        self.assertTrue(' ' not in res)
        
    def test_roles_for_users_on_users_raises_without_relevant_roles(self):
        # If for some reasons you want to enforce rules on users...
        django_user = User.objects.create(username="test", 
                                        email="test@example.com",
                                        first_name="Test",
                                        last_name = "Tester")
        user = MockUser() # That's faster
        setattr(user, 'member', True)
        with self.assertRaises(RulesException):
            res = get_roles(user, django_user)
            self.assertEqual(len(res), 1)
            
    def test_roles_for_users_on_users_works_with_relevant_roles(self):
        # If for some reasons you want to enforce rules on users...
        django_user = User.objects.create(username="test", 
                                        email="test@example.com",
                                        first_name="Test",
                                        last_name = "Tester")
        setattr(django_user, 'relevant_roles', lambda : [Tester])
        user = MockUser() # That's faster
        setattr(user, 'member', True)
        res = get_roles(user, django_user)
        self.assertEqual(len(res), 1)
            