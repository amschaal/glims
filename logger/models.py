from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from notifications.signals import notification_created
from notifications.models import Notification

class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=30) #Can be coerced into integer key if necessary
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    url = models.URLField(blank=True,null=True)
    

def CreateNotificationLog(sender,instance=None,**kwargs):
    if instance:
        ct = ContentType.objects.get_for_model(instance)
        Log.objects.create(text=kwargs['text'],description=kwargs['description'],content_type=ct,object_id=str(instance.pk),url=kwargs['url'])
notification_created.connect(CreateNotificationLog, Notification)
