from django.dispatch import Signal
from glims.middlewares.ThreadLocal import get_current_user
object_updated = Signal(providing_args=["instance","old_instance","user"])
directory_created = Signal(providing_args=["instance","directory"])

def object_updated_callback(sender,instance,**kwargs):
    if not hasattr(instance, 'id'):
        return
    try:
        old_instance = sender.objects.get(id=instance.id)
        object_updated.send(sender,instance=instance,old_instance=old_instance,user=get_current_user())
    except sender.DoesNotExist, e:
        pass
