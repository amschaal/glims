from django.db import models
from glims.lims import Lab, Project
from django.contrib.auth.models import Group
from django.utils._os import safe_join
import os
from django.conf import settings

class BioshareAccount(models.Model):
    group = models.OneToOneField(Group, related_name="bioshare_account")
    auth_token = models.CharField(max_length=100)
    def create_share(self, name, directory, description=''):
#         @todo: replace with real API call
        import string, random
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(15))

class LabShare(models.Model):
    lab = models.ForeignKey(Lab)
    group = models.ForeignKey(Group)
    bioshare_id = models.CharField(max_length=15,unique=True)
    class Meta:
        unique_together = (('lab','group'))
    def save(self, *args, **kwargs):
        if not self.bioshare_id:
            if not os.path.exists(self.directory(full=True)):
                os.makedirs(self.directory(full=True))
            self.bioshare_id = self.group.bioshare_account.create_share('%s - %s'%(self.lab.name,self.group.name),self.directory)
        return super(LabShare, self).save(*args, **kwargs)
#         return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
    def directory(self,full=True):
        path = os.path.join(self.group.name.replace(' ','_'),'labs',self.lab.slug,'share')
        print path
        if full:
            path = safe_join(settings.FILES_ROOT,path)
        return path

class ProjectShare(models.Model):
    project = models.OneToOneField(Project)
    labshare = models.ForeignKey(LabShare)
    folder = models.SlugField(max_length=50)
    class Meta:
        unique_together = (('labshare','folder'))
    def directory(self,full=True):
        return safe_join(self.labshare.directory(full=full),self.folder)
    