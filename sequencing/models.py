from __future__ import unicode_literals

from django.db import models
from glims.models import Pool
from extensible.models import ExtensibleModel
from datetime import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch.dispatcher import receiver

class Machine(models.Model):
    name = models.CharField(max_length=50,db_index=True)
    description = models.TextField(null=True,blank=True)
    num_lanes = models.SmallIntegerField()
    def __unicode__(self):
        return self.name

class Run(ExtensibleModel):
    name = models.CharField(max_length=100,blank=True,null=True,db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    machine = models.ForeignKey(Machine)
    description = models.TextField(null=True,blank=True)

class Lane(ExtensibleModel):
    run = models.ForeignKey(Run,related_name='lanes')
    index = models.PositiveSmallIntegerField()
    pool = models.ForeignKey(Pool,null=True,blank=True)
    description = models.TextField(null=True,blank=True,db_index=True)
    class Meta:
        unique_together = (('run','index'))

@receiver(pre_save,sender=Run)
def set_run_name(sender,instance,**kwargs):
    if instance.name and instance.id:
        return
    if not instance.name:
        t = instance.created or datetime.now()
        instance.name = '%s: %s' % (instance.machine.name, t.strftime('%Y-%m-%d'))

@receiver(post_save,sender=Run)
def create_run(sender,instance,created,**kwargs):
    if created:
        for i in range(1,instance.machine.num_lanes+1):
            Lane.objects.create(run=instance, index=i)