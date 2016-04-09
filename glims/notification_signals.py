from django.conf import settings
from django.db.models.signals import pre_delete, post_delete, post_save, pre_save
# from models import Order, Invoice, Account, Core, BillingGroup, Service, OrderStatus, Status, OrderItem
from django.contrib.auth.models import Group, User
from attachments.models import Note, File
# from attachments import signals as attachment_signals
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from django.db.models import Q

from notifications.utils import create_notification
from notifications.models import Notification




@receiver(post_save,sender=Note)
def create_note_notification(sender,**kwargs):
    print "FOOO!!!!!!!!!!!"
    if kwargs['created']:
        instance = kwargs['instance']
        obj = instance.content_object#ct.get_object_for_this_type(instance.object_id)
        if hasattr(obj, 'get_notification_users'):
            users = obj.get_notification_users().exclude(id=instance.created_by.id).distinct()
            print users
            url = settings.SITE_URL + obj.get_absolute_url()+'?tab=notes'
            description = '%s wrote: "%s..."'%(str(instance.created_by), instance.content[:200])
            text = '%s wrote: "%s..."'%(str(instance.created_by),instance.content[:20])
            create_notification(url,text,type_id='note_created',description=description,users=users,importance=Notification.IMPORTANCE_LOW)
        
# @receiver(post_save,sender=URL)
# def create_url_notification(sender,**kwargs):
#     if kwargs['created']:
#         instance = kwargs['instance']
#         obj = instance.content_object#ct.get_object_for_this_type(instance.object_id)
#         users = User.objects.filter(groups__in=[obj.billing_group.group.id,obj.core.group.id]).exclude(id=instance.created_by.id)
#         url = settings.SITE_URL + reverse('order',kwargs={'order_id':obj.id})+'?tab=urls'
#         description = instance.url
#         text = '%s added a url to your order'%(str(instance.created_by))
#         create_notification(url,text,type_id='url_created',description=description,users=users,importance=Notification.IMPORTANCE_LOW)

@receiver(post_save,sender=File)
def create_file_notification(sender,**kwargs):
    if kwargs['created']:
        instance = kwargs['instance']
        obj = instance.content_object#ct.get_object_for_this_type(instance.object_id)
        if hasattr(obj, 'get_notification_users'):
            users = obj.get_notification_users().exclude(id=instance.uploaded_by.id).distinct()
            url = settings.SITE_URL + obj.get_absolute_url()+'?tab=files'
            description = instance.description
            text = '%s uploaded %s'%(str(instance.uploaded_by),str(instance))
            create_notification(url,text,type_id='file_created',description=description,users=users,importance=Notification.IMPORTANCE_LOW)
