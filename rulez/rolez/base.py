#-*- coding: utf-8 -*-

class AbstractRole(object):
    """
    This is an abstract class to show what a role should look like
    """
    @classmethod
    def is_member(cls, user, obj): #pragma: nocover
        raise NotImplemented
