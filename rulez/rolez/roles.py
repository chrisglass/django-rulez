#-*- coding: utf-8 -*-

class AbstractRole(object):
    """
    This is an abstract class to show what a role should look like
    """
    def is_member(self, user, obj): #pragma: nocover
        raise NotImplemented