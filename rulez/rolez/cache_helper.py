#-*- coding: utf-8 -*-

from django.contrib.auth.models import User, AnonymousUser
from django.core.cache import cache
from rulez.exceptions import RulesException
import time

"""
Cache keys:

For the list of roles, per user, per instance:
<prefix>-<user.id>-<user counter>-<obj.type>-<obj.id>-<obj counter>

For the counter , per instance:
<prefix>-<obj.type>-<obj.id>

"""

HOUR = 60*60

#===============================================================================
# Counter handling
#===============================================================================
def counter_key(obj):
    if obj.__class__ in (User, AnonymousUser,):
        pk = get_user_pk(obj)
    else:
        pk = obj.pk
    obj_type = str(obj.__class__.__name__).lower()
    return "%s-%s" % (obj_type, pk)


def increment_counter(obj):
    """
    Invalidate the cache for the passed object.
    """
    if obj is not None: # If the object is None, do nothing (it's pointless)
        cache.set(counter_key(obj), int(time.time()), 1*HOUR)


def get_counter(obj):
    """
    Returns the cached counter for the given object instance
    """
    counter = cache.get(counter_key(obj))
    if not counter:
        counter = 0
    return counter


def roles_key(user, obj):
    if obj.__class__ in (User, AnonymousUser,):
        obj_id = get_user_pk(obj)
    else:
        obj_id = obj.pk
    obj_type = str(obj.__class__.__name__).lower()
    obj_counter = get_counter(obj)
    user_id = get_user_pk(user)
    user_counter = get_counter(user)
    return "%s-%s-%s-%s-%s" % (user_id, user_counter, obj_type, obj_id,
                               obj_counter)


def get_user_pk(user):
    if not user or (user and user.is_anonymous()):
        return 'anonymous'
    else:
        return user.pk

#===============================================================================
# Main function
#===============================================================================

def get_roles(user, obj):
    """
    Get a list of roles assigned to a user for a specific instance from the
    cache, or builds such a list if it is not found.
    """
    # get roles for the user, if present:
    roles = cache.get(roles_key(user, obj))
    if isinstance(roles, list):
        # Cache hit (a miss returns NoneType rather than an empty list)
        return roles
    else:
        # we need to recompute roles for this model
        user_roles = []
        if not hasattr(obj, 'relevant_roles'):
            raise RulesException(
                'Cannot build roles cache for %s instance. Did you forget to \
                define a "relevant_roles()" method on %s?' % (obj.__class__,
                                                              obj.__class__))

        relevant = obj.relevant_roles()
        for role in relevant:
            if role.is_member(user, obj):
                user_roles.append(role)
        cache.set(roles_key(user, obj), user_roles, 1*HOUR)
        return user_roles
