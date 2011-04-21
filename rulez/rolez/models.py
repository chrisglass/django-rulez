#-*- coding: utf-8 -*-
from rulez.rolez.cache_helper import get_roles, increment_counter
import signals

class ModelRoleMixin(object):
    """
    This adds roles-handling methods to the model it's mixed with
    """
    
    def get_roles(self, user):
        """
        Gets all roles this user has for this object and caches it on the
        instance.
        Without the instance cache every call to has_role() would hit the
        cache backend.
        """
        rolez = getattr(self, '_rolez', {})
        if not user.pk in rolez.keys():
            rolez[user.pk] = get_roles(user, self)
        self._rolez = rolez
        return self._rolez[user.pk]
    
    def has_role(self, user, role):
        """
        Checks wether the passed user is a member of the passed role for the
        passed instance
        """
        roles = self.get_roles(user)
        if role in roles:
            return True
        return False
    
    def relevant_roles(self):
        """
        Returns a list of roles *classes* relevant to this instance type.
        This is to optimise the building of the user's roles in case of cache 
        miss
        """
        return self.roles
    
    def rulez_invalidate(self):
        """
        This is the default, simple case where the model is related to user, and
        so invalidating it will force connected users to recalculate their keys
        
        In some cases you will want to invalidate the related objects here by 
        incrementing counters for other models in your application
        """
        increment_counter(self)
