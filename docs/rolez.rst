==================
Using roles
==================

Writing a new role
==================

Just as writing new object-level permissions is really easy with django-rulez,
we wanted to provide a simple way to handle user roles.

Writing a role consists of doing the following::

  class GuestRole(object):
    def is_member(user, object):
        """Determine wether the passed user is a member of this group"""
        if user.is_anonymous:
            return True:
        else:
            return False

That's it! a role must simply be a class defining an "is_member" method that
accepts a user and an object instace, and the role must answer True or False,
depending on wether the passed user is a member of the group or not.

