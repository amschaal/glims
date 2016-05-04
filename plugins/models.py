from django.db import models
from extensible.models import ModelType

class Plugin(models.Model):
    id = models.CharField(max_length=30,primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    def __unicode__(self):
        return self.name
    
class ModelTypePlugin(models.Model):
    type = models.ForeignKey(ModelType)
    plugin = models.ForeignKey(Plugin)
    order = models.PositiveSmallIntegerField(default=1)
    class Meta:
        unique_together = ('type','plugin')
    