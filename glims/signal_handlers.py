from django.conf import settings
from django.db.models.signals import post_save, pre_save,\
    m2m_changed
from django.contrib.auth.models import User
from attachments.models import Note, File
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from notifications.utils import create_notification
from notifications.models import Notification, UserSubscription
from glims.lims import Project
from glims.signals import object_updated


@receiver(m2m_changed,sender=Project.participants.through)
def update_participant_subscriptions(sender,instance,pk_set,**kwargs):
    print 'update participant subscriptions'
    print kwargs
    if kwargs.pop('action',None) == 'post_add': 
        project_type = ContentType.objects.get_for_model(Project)
        for user in User.objects.filter(pk__in=pk_set):
            subscription, created = UserSubscription.objects.get_or_create(user=user,content_type=project_type,object_id=instance.id)
    
@receiver(object_updated,sender=Project)
def update_manager_subscription(sender,instance,old_instance,**kwargs):
    if instance.manager != old_instance.manager:
        project_type = ContentType.objects.get_for_model(Project)
        subscription, created = UserSubscription.objects.get_or_create(user=instance.manager,content_type=project_type,object_id=instance.id)


"""
Signal handlers for notifications below
"""

@receiver(post_save,sender=Note)
def create_note_notification(sender,**kwargs):
    print "FOOO!!!!!!!!!!!"
    if kwargs['created']:
        instance = kwargs['instance']
        obj = instance.content_object#ct.get_object_for_this_type(instance.object_id)
#         if hasattr(obj, 'get_notification_users'):
#             users = obj.get_notification_users().exclude(id=instance.created_by.id).distinct()
        url = settings.SITE_URL + obj.get_absolute_url()+'?tab=notes'
        description = '%s wrote: "%s..."'%(str(instance.created_by), instance.content[:200])
        text = '%s: %s wrote "%s..."'%(str(obj),str(instance.created_by),instance.content[:20])
        create_notification(url,text,type_id='note_created',description=description,instance=obj,importance=Notification.IMPORTANCE_LOW,exclude_user=instance.created_by)
        

@receiver(post_save,sender=File)
def create_file_notification(sender,**kwargs):
    if kwargs['created']:
        instance = kwargs['instance']
        obj = instance.content_object#ct.get_object_for_this_type(instance.object_id)
#         if hasattr(obj, 'get_notification_users'):
#             users = obj.get_notification_users().exclude(id=instance.uploaded_by.id).distinct()
        url = settings.SITE_URL + obj.get_absolute_url()+'?tab=files'
        description = instance.description
        text = '%s: %s uploaded %s'%(str(obj),str(instance.uploaded_by),str(instance))
        create_notification(url,text,type_id='file_created',description=description,instance=obj,importance=Notification.IMPORTANCE_LOW,exclude_user=instance.uploaded_by)

@receiver(pre_save,sender=Project)
def create_update_notification(sender, instance,**kwargs):
    try:
        pre_update = sender.objects.get(id=instance.id)
        changed = []
        print instance._meta.get_fields()
        for field in instance._meta.get_fields():
            if field.name in ['status','history']:
                continue
            if getattr(pre_update, field.name,None) != getattr(instance, field.name,None):
                changed.append(field.name)
        if len(changed) > 0:
            url = settings.SITE_URL + instance.get_absolute_url()
            text = '"%s" has been updated'%(str(instance))
            description = "The following fields have been modified: %s" % ', '.join(changed)
            create_notification(url,text,type_id='object_updated',description=description,instance=instance,importance=Notification.IMPORTANCE_LOW)
    except sender.DoesNotExist, e:
        pass

