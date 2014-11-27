from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Attach a file to just about anything:
# file = File(text='My wonderful note',created_by=request.user,content_object=some_model_instance)
# file.save()
class File(models.Model):
    file = models.FileField(upload_to='files')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    uploaded_by = models.ForeignKey(User,null=True,blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=30) #Can be coerced into integer key if necessary
    content_object = GenericForeignKey('content_type', 'object_id')
    admin_only = models.BooleanField(default=True)
    def __unicode__(self):              # __unicode__ on Python 2
        return self.file.name[:30]+'...'
    
class Note(models.Model):
    parent = models.ForeignKey('Note',null=True,blank=True)
    content = models.TextField()
    created_by = models.ForeignKey(User,null=True,blank=True, related_name='notes')
    created = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User,null=True,blank=True, related_name='+')
    modified = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=30) #Can be coerced into integer key if necessary
    content_object = GenericForeignKey('content_type', 'object_id')
    admin_only = models.BooleanField(default=True)
    def __unicode__(self):              # __unicode__ on Python 2
        return self.content[:50]+'...'
