# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings

from models import Dummy
from rulez.exceptions import NonexistentFieldName
from rulez.exceptions import NotBooleanPermission
from rulez import registry

class BackendTest(TestCase):
    def setUp(self):
        try:
            self.anonymous = User.objects.get_or_create(id=settings.ANONYMOUS_USER_ID, username='anonymous', is_active=True)[0]
        except Exception:
            self.fail("You need to define an ANONYMOUS_USER_ID in your settings file")
        
        self.user = User.objects.get_or_create(username='javier', is_active=True)[0]
        self.otherUser = User.objects.get_or_create(username='juan', is_active=True)[0]
        self.superuser = User.objects.get_or_create(username='miguel', is_active=True, is_superuser=True)[0]
        self.not_active_superuser = User.objects.get_or_create(username='rebeca', is_active=False, is_superuser=True)[0]
        self.obj = Dummy.objects.get_or_create(supplier=self.user)[0]
#        self.ctype = ContentType.objects.get_for_model(self.obj)
        
        registry.register(codename='can_ship', field_name='canShip', model=self.obj.__class__, view_param_pk='idDummy',
                                            description="Only supplier have the authorization to ship")

    
    def test_regularuser_has_perm(self):
        self.assertTrue(self.user.has_perm('can_ship', self.obj))
    
    def test_regularuser_has_not_perm(self):
        self.assertFalse(self.otherUser.has_perm('can_ship', self.obj))
    
    def test_superuser_has_perm(self):
        self.assertTrue(self.superuser.has_perm('invented_perm', self.obj))

    def test_object_none(self):
        self.assertFalse(self.user.has_perm('can_ship'))
    
    def test_anonymous_user(self):
        anonymous_user = AnonymousUser()
        self.assertFalse(anonymous_user.has_perm('can_ship', self.obj))

    def test_not_active_superuser(self):
        self.assertFalse(self.not_active_superuser.has_perm('can_ship', self.obj))

    def test_nonexistent_perm(self):
        self.assertFalse(self.user.has_perm('nonexistent_perm', self.obj))

    def test_nonboolean_method(self):
        registry.register(codename='wrong_rule', field_name='methodInteger', model=self.obj.__class__, view_param_pk='idDummy',
                                            description="Wrong rule. The field_name exists so It is created, but it does not return True or False")
        
        self.assertRaises(NotBooleanPermission, lambda:self.user.has_perm('wrong_rule', self.obj))
    
    def test_nonexistent_field_name(self):
        # Dinamycally removing canShip from class Dummy to test an already existent rule that doesn't have a valid field_name anymore
        fun = Dummy.canShip
        del Dummy.canShip
        self.assertRaises(NonexistentFieldName, lambda:self.user.has_perm('can_ship', self.obj))
        Dummy.canShip = fun

    def test_has_perm_method_no_parameters(self):
        registry.register(codename='canTrash', field_name='canTrash', model=self.obj.__class__, view_param_pk='idDummy',
                                            description="Rule created from a method that gets no parameters")

        self.assertTrue(self.user.has_perm('canTrash', self.obj))

class UtilsTest(TestCase):
    def test_register_valid_rules(self):
        rules_list = [
            # Dummy model
            {'codename':'can_ship', 'model':Dummy, 'field_name':'canShip', 'view_param_pk':'idView', 'description':"Only supplier has the authorization to ship"},
        ]
        for params in rules_list:
            registry.register(**params)

    def test_register_invalid_rules_NonexistentFieldName(self):
        rules_list = [
            # Dummy model
            {'codename':'can_ship', 'model':Dummy, 'field_name':'canSship', 'view_param_pk':'idView', 'description':"Only supplier has the authorization to ship"},
        ]
        for params in rules_list:
            self.assertRaises(NonexistentFieldName, lambda: registry.register(**params))

    def test_register_valid_rules_compact_style(self):
        rules_list = [
            # Dummy model
            {'codename':'canShip', 'model':Dummy},
        ]
        for params in rules_list:
            registry.register(**params)

