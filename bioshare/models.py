from django.db import models
from glims.lims import Lab, Project
from django.contrib.auth.models import Group
from django.utils._os import safe_join
import os
from django.conf import settings
from django.db.models.signals import post_save, pre_save
import shutil
import urllib2
import json
from bioshare.utils import get_real_files, get_symlinks

class BioshareAccount(models.Model):
    group = models.OneToOneField(Group, related_name="bioshare_account")
    auth_token = models.CharField(max_length=100)
    def __unicode__(self):
        return 'Bioshare account: %s'%self.group.name
    def create_share(self, name, directory, description=None):
#         @todo: replace with real API call
#         import string, random
#         return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(15))
        description = description or 'Genome Center LIMS generated share'
        req = urllib2.Request(settings.BIOSHARE_SETTINGS['CREATE_URL'])
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', 'Token %s'%self.auth_token)
        filesystem = settings.BIOSHARE_SETTINGS['DEFAULT_FILESYSTEM']
        params = {"name":name,"notes":description,"filesystem":filesystem,"link_to_path":directory,'read_only':True}
        try:
            response = urllib2.urlopen(req, json.dumps(params))
            if response.getcode() == 200:
                data = json.load(response)
                return data['id']
            else:
                raise Exception('Unable to create Bioshare share')
        except urllib2.HTTPError as e:
            error_message = e.read()
            print error_message
            raise Exception('Unable to create share: %s'%error_message)
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
            self.bioshare_id = self.group.bioshare_account.create_share('%s - %s'%(self.lab.name,self.group.name),self.directory())
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
    #This should always return an empty array.  We don't want actual data, just a view on the data!
    def real_files(self,relpath=True):
        return get_real_files(self.directory(full=True),relpath)
    def symlinks(self,relpath=True):
        return get_symlinks(self.directory(full=True),relpath)

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
    