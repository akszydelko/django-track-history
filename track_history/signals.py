from __future__ import unicode_literals
from django.db.models.signals import ModelSignal, post_init, post_save, post_delete

th_post_init_deferred = ModelSignal(providing_args=["instance"], use_caching=True)
th_post_save_deferred = ModelSignal(providing_args=["instance", "created", "using", "update_fields"], use_caching=True)
# TODO: Delete called on deferred model

post_init_signals = [post_init, th_post_init_deferred]
save_signals = [post_save, th_post_save_deferred]
delete_signals = [post_delete]
