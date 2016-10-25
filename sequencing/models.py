from __future__ import unicode_literals

from django.db import models
from glims.models import Pool
from extensible.models import ExtensibleModel

class Machine(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    def __unicode__(self):
        return self.name

class Run(ExtensibleModel):
    created = models.DateTimeField(auto_now_add=True)
    machine = models.ForeignKey(Machine)
    description = models.TextField(null=True,blank=True)

class Lane(ExtensibleModel):
    run = models.ForeignKey(Run,related_name='lanes')
    index = models.PositiveSmallIntegerField()
    pool = models.ForeignKey(Pool,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    class Meta:
        unique_together = (('run','index'))