=============================
Writing simple rules
=============================

Generally speaking, django rulez maps permissions to methods on objects, so
that calling user.has_perm("my_perm", obj) will call the my_perm method on the
object, that should return either True or False.

Let's look at a quick example::

    from rulez import registry

    class Book(object):
        ...

        def can_read(self, user):
            if user.is_athenticated:
                return True
            else:
                return False
    registry.register("can_read", Book)


In this simplistic example, a user only has the "can_read" permission if he is
not anonymous.
