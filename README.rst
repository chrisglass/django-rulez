#############
django-rulez
#############

django-rulez is a fork of django-rules, since some of the goals django-rules set themselves didn't match our current
project goals.You can refer to their github project page for more information about this cool project: https://github.com/maraujop/django-rules
Kudos for the good work guys!

Generally, it is a per-object authorization backend, that stores the rules themselves as methods on model.

Installation
=============


From source
------------

To install django-rulez from source::

	git clone https://github.com/cglass/django-rulez/ django-rulez
	cd django-rulez
	python setup.py install

From Pypi
----------

Simply install django-rulez like you would install any other pypi package::

    pip install django-rulez


Configuration
==============

* Add it to the list of `INSTALLED_APPS` in your `settings.py`
* Add the django-rulez authorization backend to the list of `AUTHENTICATION_BACKENDS` in `settings.py`::

	AUTHENTICATION_BACKENDS = {
	    'django.contrib.auth.backends.ModelBackend', # Django's default auth backend
	    'django_rules.backends.ObjectPermissionBackend',
	}

Example
=========

The following example should get you started::

    # models.py
    from rulez import registry
    
    class myModel(models.Model)
        
        def can_edit(self, user_obj):
            '''
            Not a very useful rule, but it's an example
            '''
            if user_obj.username == 'chris':
                return True
            return False
            
    registry.register('can_edit', myModel)

