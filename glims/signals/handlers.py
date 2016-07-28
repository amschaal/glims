from datetime import datetime
import os
import shutil
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save, \
    m2m_changed, post_delete
from django.dispatch import receiver

from attachments.models import Note, File, delete_attachments
from glims.lims import Project, Sample, Pool
from glims.signals.signals import object_updated, object_updated_callback
from notifications.models import Notification, UserSubscription
from notifications.utils import create_notification


@receiver(pre_save,sender=Project)
def handle_status(sender,instance,**kwargs):
    if not hasattr(instance, 'id'):
        return
    if not instance.history.has_key('statuses'):
        instance.history['statuses'] = []
    try:
        old = Project.objects.get(id=instance.id)
        if old.status != instance.status:
            instance.history['statuses'].append({'name':instance.status.name,'id':instance.status.id,'updated':datetime.now().isoformat()})
    except Project.DoesNotExist, e:
        if instance.status:
            instance.history['statuses'].append({'name':instance.status.name,'id':instance.status.id,'updated':datetime.now().isoformat()})

#This could be avoided if the directory structures only depended on immutable values!!!
@receiver(object_updated,sender=Project)
def update_project_directory(sender,instance,old_instance,**kwargs):
    old_directory = old_instance.directory(full=True)
    new_directory = instance.directory(full=True)
    if old_directory != new_directory and os.path.isdir(old_directory):
        shutil.move(old_directory, new_directory)
        for file in File.objects.filter(file__startswith=old_directory,object_id=instance.id, issue_ct=ContentType.objects.get_for_model(Project)):
            file.file.name = file.file.name.replace(old_directory,new_directory)
            file.save()


@receiver(post_save,sender=Project)
def create_project_directories(sender,instance,**kwargs):
    instance.create_directories()

pre_save.connect(object_updated_callback, sender=Project)
pre_save.connect(object_updated_callback, sender=Sample)
pre_save.connect(object_updated_callback, sender=Pool)

post_delete.connect(delete_attachments, sender=Project)
post_delete.connect(delete_attachments, sender=Sample)
post_delete.connect(delete_attachments, sender=Pool)

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

