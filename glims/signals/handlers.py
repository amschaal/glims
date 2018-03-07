from datetime import datetime
import os
import shutil
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save, \
    m2m_changed, post_delete
from django.dispatch import receiver

from attachments.models import Note, File, delete_attachments
from glims.models import Project, Sample, Pool, Lab, Library
from glims.signals.signals import object_updated, object_updated_callback
from notifications.models import Notification, UserSubscription
from notifications.utils import create_notification
from glims.middlewares.ThreadLocal import get_current_user
from notifications.signals import notification_created
from django.utils import timezone


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
#         for file in File.objects.filter(file__startswith=old_directory,object_id=instance.id, issue_ct=ContentType.objects.get_for_model(Project)):
#             file.file.name = file.file.name.replace(old_directory,new_directory)
#             file.save()

@receiver(object_updated,sender=Lab)
def update_lab_directories(sender,instance,old_instance,**kwargs):
    for g in Group.objects.all():
        old_directory = old_instance.get_group_directory(g,full=True)
        new_directory = instance.get_group_directory(g,full=True)
        if old_directory != new_directory and os.path.isdir(old_directory):
            shutil.move(old_directory, new_directory)
#             for file in File.objects.filter(file__startswith=old_directory,object_id=instance.id, issue_ct=ContentType.objects.get_for_model(Project)):
#                 file.file.name = file.file.name.replace(old_directory,new_directory)
#                 file.save()

@receiver(object_updated,sender=Sample)
def update_sample_directory(sender,instance,old_instance,**kwargs):
    old_directory = old_instance.directory(full=True)
    new_directory = instance.directory(full=True)
    if old_directory != new_directory and os.path.isdir(old_directory):
        shutil.move(old_directory, new_directory)


@receiver(post_save,sender=Project)
def create_project_directories(sender,instance,created,**kwargs):
    if created:
        print "Create project directories"
        instance.create_directories()

pre_save.connect(object_updated_callback, sender=Project)
pre_save.connect(object_updated_callback, sender=Sample)
pre_save.connect(object_updated_callback, sender=Pool)
pre_save.connect(object_updated_callback, sender=Lab)

post_delete.connect(delete_attachments, sender=Project)
post_delete.connect(delete_attachments, sender=Sample)
post_delete.connect(delete_attachments, sender=Pool)

@receiver(m2m_changed,sender=Project.participants.through)
def update_participant_subscriptions(sender,instance,pk_set,**kwargs):
    if kwargs.pop('action',None) == 'post_add': 
        project_type = ContentType.objects.get_for_model(Project)
        for user in User.objects.filter(pk__in=pk_set):
            subscription, created = UserSubscription.objects.get_or_create(user=user,content_type=project_type,object_id=instance.id)
            subscription.subscribed = True
            subscription.save()

@receiver(post_save,sender=Project)
def set_manager_subscription(sender,instance,created,**kwargs):
    if instance.manager:
        project_type = ContentType.objects.get_for_model(Project)
        subscription, created = UserSubscription.objects.get_or_create(user=instance.manager,content_type=project_type,object_id=instance.id)
        subscription.subscribed = True
        subscription.save()
@receiver(pre_save,sender=Lab)
def set_lab_slug(sender,instance,**kwargs):
    if not instance.slug:
        instance.slug = instance.get_directory_name()
        
@receiver(pre_save,sender=Library)
def set_library_name(sender,instance,**kwargs):
    if instance.name and instance.id:
        return
    if not instance.name:
        instance.name = instance.sample.sample_id
    for i in range(1,100):
        new_name = '%s-%d'%(instance.sample.sample_id,i)
        if not Library.objects.filter(name=new_name).first():
            instance.name = new_name
            break
            
        
    
    
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
        url = obj.get_absolute_url()+'?tab=notes'
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
        url = obj.get_absolute_url()+'?tab=files'
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
            url = instance.get_absolute_url()
            text = '"%s" has been updated'%(str(instance))
            description = "The following fields have been modified: %s" % ', '.join(changed)
            create_notification(url,text,type_id='object_updated',description=description,instance=instance,importance=Notification.IMPORTANCE_LOW,exclude_user=get_current_user())
        #Send notification to new manager
        if instance.manager and instance.manager != pre_update.manager:
            create_notification(url,'%s has been assigned manager for project %s'%(instance.manager,instance),instance=instance,importance=Notification.IMPORTANCE_LOW,users=[instance.manager.id])#,exclude_user=get_current_user()
    except sender.DoesNotExist, e:
        pass

#Any time a notification is created for a project, update the modified date.
def UpdateProjectModified(sender,instance=None,**kwargs):
    if isinstance(instance, Project):
        Project.objects.filter(id=instance.id).update(modified=timezone.now())
notification_created.connect(UpdateProjectModified, Notification)