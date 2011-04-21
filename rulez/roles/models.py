#-*- coding: utf-8 -*-
from rulez.roles.cache_helper import get_roles

class ModelRoleMixin(object):
    """
    This adds roles-handling methods to the model it's mixed with
    """
    
    def has_role(self, user, role):
        """
        Checks wether the passed user is a member of the passed role for the
        passed instance
        """
        roles = get_roles(user, self)
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