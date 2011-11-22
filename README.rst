#############
django-rulez
#############

django-rulez is a lean, fast and complete rules-based permissions system for
the django framework.

Most other authentication frameworks focus on using database joins, which gets
pretty slow after a while (since mostly every query generates a lot of joins).
Django-rulez uses a memory-based hashmap instead.

Django-rulez also implements a role concept, allowing for very readable and
maintainable code.

django-rulez was forked from django-rules, since some of the goals django-rules
set themselves didn't match our current project goals.You can refer to their 
github project page for more information about this other cool project: 
https://github.com/maraujop/django-rules
Kudos for the good work guys!

Generally, it is also an instance-level authorization backend, that stores the 
rules themselves as methods on models.

Installation
=============


From source
------------

To install django-rulez from source::

	git clone https://github.com/chrisglass/django-rulez/ django-rulez
	cd django-rulez
	python setup.py install

From Pypi
----------

Simply install django-rulez like you would install any other pypi package::

    pip install django-rulez


Configuration
==============

* Add `rulez` to the list of `INSTALLED_APPS` in your `settings.py`
* Add the django-rulez authorization backend to the list of `AUTHENTICATION_BACKENDS` in `settings.py`::

	AUTHENTICATION_BACKENDS = [
	    'django.contrib.auth.backends.ModelBackend', # Django's default auth backend
	    'rulez.backends.ObjectPermissionBackend',
	]

Example
=========

The following example should get you started::

    # models.py
    from rulez import registry
    
    class myModel(models.Model):
        
        def can_edit(self, user_obj):
            '''
            Not a very useful rule, but it's an example
            '''
            if user_obj.username == 'chris':
                return True
            return False
            
    registry.register('can_edit', myModel)

Django-rulez requires to declare the rule as a method in the same model. This
is very simple in case the rule applies to a model in our own application, but
in some cases, we might need to set object permisions to models from 3rd-party
applications (e.g. to the User model). Let's see an example for this case::

    # models.py
    from django.contrib.auth.models import User
    from rulez import registry
    
    def user_can_edit(self, user_obj):
        '''
        This function will be hooked up to the User model as a method.
        The rule says that a user can only be modified by the same user
        '''
        if self == user_obj:
            return True
        return False
    
    # 'add_to_class' is a standard Django method
    User.add_to_class('can_edit', user_can_edit)
            
    registry.register('can_edit', User)

Another example: using roles
=============================

A little more code is needed to use roles, but it's still pretty concise::

    # models.py
    from rulez.rolez.base import AbstractRole
    from rulez import registry

    class Editor(AbstractRole):
        """ That's a role"""
        @classmethod
        def is_member(cls, user, obj):
            """Remember, class methods take the class instead of self"""
            if user.username == 'chris':
                return True
            return False

    class myModel(models.Model, ModelRoleMixin): # Don't forget the mixin!
        
        def can_edit(self, user_obj):
            '''
            Not a very useful either but it's an example
            '''
            return self.has_role(user_obj, Editor):

    registry.register('can_edit', myModel)
