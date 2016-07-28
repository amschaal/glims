from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from glims.models import Project

# Create your models here.
class Task(models.Model):
    STATUS_WAITING = 'waiting'
    STATUS_DONE = 'done'
    STATUS_ACTIVE = 'active'
    STATUS_OPTIONS = ((STATUS_WAITING,'Waiting'),(STATUS_ACTIVE,'Active'),(STATUS_DONE,'Done'))
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project)
    dependencies = models.ManyToManyField('self',symmetrical=False,related_name='dependents',null=True,blank=True)
    name = models.CharField(max_length=50)
    content = models.TextField(null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
    created_by = models.ForeignKey(User,null=True,blank=True, related_name='+')
    created = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User,null=True,blank=True, related_name='+')
    modified = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User,null=True,blank=True,related_name='tasks')
    status = models.CharField(max_length=30,null=True,blank=True)
    #A generic relation could be useful if the milestone should relate to a pool or something....
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.CharField(max_length=30) #Can be coerced into integer key if necessary
#     content_object = GenericForeignKey('content_type', 'object_id')
    def __unicode__(self):              
        return self.name[:50]+'...'