from __future__ import unicode_literals

from django.db import models
from glims.models import Pool

class Run(models.Model):
    created = models.DateTimeField(auto_now_add=True)

class Lane(models.Model):
    run = models.ForeignKey(Run)
    pool = models.ForeignKey(Pool)