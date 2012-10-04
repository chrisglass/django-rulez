

class rules(object):
    """
    On a decorated class; registers all passed permission names with this
    object; or, if no names are passed, registers all can_FOO functions.
    """

    def __init__(self, *args):
        # Names of the functions to register when the class object
        # is created.
        self.codenames = args

    def __call__(self, cls):
        import inspect
        from . import registry

        if not self.codenames:
            # No codenames were passed; register all can_FOO functions
            for codename, unused in inspect.getmembers(cls):
                if codename.startswith('can_'):
                    registry.register(codename, cls)
        else:
            # Register all provided names
            for codename in self.codenames:
                registry.register(codename, cls)

        # Pass it along
        return cls
