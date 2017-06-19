from __future__ import unicode_literals

from django.db import models
from glims.models import Project
from django.conf import settings
from django.contrib.auth.models import User

"""
    Must define ACCOUNT_TYPES in config.py
    ACCOUNT_TYPES = (('DAFIS','DaFIS Account'),('PO','Purchase Order')) 
"""

class Category(models.Model):
    name = models.CharField(max_length=50)
    
class Log(models.Model):
    STATUS_NOT_BILLED = 'Not billed'
    STATUS_BILLED = 'Billed'
    STATUS_NOT_BILLABLE = 'Not Billable'
    STATUS_CHOICES = ((STATUS_NOT_BILLED,STATUS_NOT_BILLED),(STATUS_BILLED,STATUS_BILLED),(STATUS_NOT_BILLABLE,STATUS_NOT_BILLABLE),)
    user = models.ForeignKey(User)
    quantity = models.FloatField()
    category = models.ForeignKey(Category)
    description = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project,related_name='tracker_logs')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=STATUS_NOT_BILLED)
    
class Export(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    modified = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True,blank=True)
    logs = models.ManyToManyField(Log,related_name='exports')
    