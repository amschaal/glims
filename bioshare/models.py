from django.db import models
from glims.lims import Lab, Project
from django.contrib.auth.models import Group
from django.utils._os import safe_join
import os
from django.conf import settings
from django.db.models.signals import post_save, pre_save
import shutil

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
        unique_together = (('labshare','folder'),('project','labshare'))
    def directory(self,full=True):
        return safe_join(self.labshare.directory(full=full),self.folder)

def create_project_share_directory(sender,instance,**kwargs):
    if hasattr(instance, 'id'):
        try:
            old = sender.objects.get(id=instance.id)
            old_directory = old.directory()
            new_directory = instance.directory()
            if old_directory != new_directory and os.path.isdir(old_directory):
                shutil.move(old_directory, new_directory)
        except:
            pass
    if not os.path.exists(instance.directory()):
        os.makedirs(instance.directory())
pre_save.connect(create_project_share_directory, ProjectShare)
    