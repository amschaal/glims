from django.dispatch import Signal
object_updated = Signal(providing_args=["instance","old_instance"])
directory_created = Signal(providing_args=["instance","directory"])

def object_updated_callback(sender,instance,**kwargs):
    if not hasattr(instance, 'id'):
        return
    try:
        old_instance = sender.objects.get(id=instance.id)
        object_updated.send(sender,instance=instance,old_instance=old_instance)
    except sender.DoesNotExist, e:
        pass
