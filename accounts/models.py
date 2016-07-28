from __future__ import unicode_literals

from django.db import models
from glims.models import Project
from django.conf import settings

"""
    Must define ACCOUNT_TYPES in config.py
    ACCOUNT_TYPES = (('DAFIS','DaFIS Account'),('PO','Purchase Order')) 
"""

class Account(models.Model):
    project = models.ForeignKey(Project, related_name="accounts")
    account = models.CharField(max_length=100,null=True,blank=True)
    type = models.CharField(max_length=25,choices=settings.ACCOUNT_TYPES)
    description = models.TextField(null=True,blank=True)