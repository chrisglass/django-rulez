# -*- coding: utf-8 -*-
import inspect

from django.conf import settings
from django.contrib.auth.models import User

from exceptions import NotBooleanPermission
from exceptions import NonexistentFieldName

from rulez import registry

class ObjectPermissionBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    def authenticate(self, username, password):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        """
        This method checks if the user_obj has perm on obj. Returns True or False
        Looks for the rule with the code_name = perm and the content_type of the obj
        If it exists returns the value of obj.field_name or obj.field_name() in case
        the field is a method.
        """
        
        if obj is None:
            return False

        if not user_obj.is_authenticated():
            user_obj = User.objects.get(pk=settings.ANONYMOUS_USER_ID)

        # We get the rule data from our registry
        rule = registry.get(perm, obj.__class__)
        if rule == None:
            return False

        bound_field = None
        try:
            bound_field = getattr(obj, rule.field_name)
        except AttributeError:
            raise NonexistentFieldName("Field_name %s from rule %s does not longer exist in model %s. \
                                        The rule is obsolete!", (rule.field_name, rule.codename, rule.model))

        if not callable(bound_field):
            raise NotBooleanPermission("Attribute %s from model %s on rule %s is not callable",
                                        (rule.field_name, rule.model, rule.codename))

        # Otherwise it is a callabe bound_field
        # Let's see if we pass or not user_obj as a parameter
        if (len(inspect.getargspec(bound_field)[0]) == 2):
            is_authorized = bound_field(user_obj)
        else:
            is_authorized = bound_field()

        if not isinstance(is_authorized, bool):
            raise NotBooleanPermission("Callable %s from model %s on rule %s does not return a boolean value",
                                        (rule.field_name, rule.model, rule.codename))

        return is_authorized
