from __future__ import unicode_literals

from django.db import models
from glims.models import Pool
from extensible.models import ExtensibleModel
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver

class Machine(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    def __unicode__(self):
        return self.name

class Run(ExtensibleModel):
    name = models.CharField(max_length=100,blank=True,null=True)
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

@receiver(pre_save,sender=Run)
def set_run_name(sender,instance,**kwargs):
    if instance.name and instance.id:
        return
    if not instance.name:
        instance.name = '%s - %s' % (instance.machine.name, instance.machine.created.strftime('%Y-%m-%d'))
