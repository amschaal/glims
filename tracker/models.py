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
    user = models.ForeignKey(User)
    quantity = models.FloatField()
    category = models.ForeignKey(Category)
    description = models.TextField(null=True,blank=True)
    modified = models.DateTimeField(auto_now=True)

class Export(models.Model):
    STATUS_NEW = 'New'
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User)
    modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50,default=STATUS_NEW)
    description = models.TextField(null=True,blank=True)
    