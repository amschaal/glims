from django.db import models
import jsonfield
from django_cloudstore.engines.bioshare import BioshareStorageEngine

class CloudStore(models.Model):
    storage_engine = models.CharField(max_length=50)
    name = models.CharField(max_length=250)
    description = models.TextField()
    url = models.URLField(null=True,blank=True)
    attributes = jsonfield.JSONField()
    def __unicode__(self):
        return "%s: %s" % (self.storage_engine, self.name)
    def __init__(self,*args,**kwargs):
        super(CloudStore, self).__init__(*args,**kwargs)
        self._engine = None
    @property
    def engine(self):
        if self._engine is None:
            if self.storage_engine == BioshareStorageEngine.ENGINE_ID:
                self._engine = BioshareStorageEngine(self)
        return self._engine
    @staticmethod
    def create(storage_engine,name,description,attributes={}):
        return storage_engine.create(name,description,attributes)
        
        