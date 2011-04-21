#-*- coding: utf-8 -*-
from django.db.models import signals

def should_we_invalidate_rolez(sender, instance, **kwargs):
    if hasattr(instance, 'rulez_invalidate'):
        instance.rulez_invalidate()
    
signals.post_save.connect(should_we_invalidate_rolez)
signals.post_delete.connect(should_we_invalidate_rolez)
