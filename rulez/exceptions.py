# -*- coding: utf-8 -*-
"""
Exceptions used by django-rules. All internal and rules-specific errors
should extend RulesError class
"""

class RulesException(Exception):
    pass

class NonexistentPermission(RulesException):
    pass

class NonexistentFieldName(RulesException):
    pass

class NotBooleanPermission(RulesException):
    pass
