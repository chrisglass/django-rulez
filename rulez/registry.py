# -*- coding: utf-8 -*-
from rulez.exceptions import NonexistentFieldName

class Rule(object):
    def __init__(self, codename, model, field_name='', view_param_pk='', 
                 description=''):
        self.field_name = field_name 
        self.description = description
        self.codename = codename
        self.model = model
        self.view_param_pk = view_param_pk

# {class: 
#    {'codename': 
#        [field_name,view_param_pk, description] 
#    } 
# } 
registry = {}
    
def register(codename, model, field_name='', view_param_pk='', description=''):
    """
    This should be called from your models.py or wherever after your models are
    declared (think admin registration)
    """
    
    # Sanity check
    if not field_name:
        field_name = codename
        
    if not hasattr(model,field_name):
        raise NonexistentFieldName('Field %s does not exist on class %s' % (field_name,model.__name__))
    
    if not model in registry.keys():
        registry[model] = {}
        
    registry[model].update({codename  : Rule(codename, model, field_name, 
                                             view_param_pk, description)})
    
def get(codename, model):
    return registry.get(model, {}).get(codename, None)
