from django.db import models
from glims.models import Lab, Project
from django.contrib.auth.models import Group
from django.utils._os import safe_join
import os
from django.db.models.signals import post_save, pre_save
import shutil
import urllib2
import json
from bioshare.utils import get_real_files, get_symlinks, remove_sub_paths
from bioshare import CREATE_URL, VIEW_URL
from django.conf import settings


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
        req = urllib2.Request(CREATE_URL)
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
                raise Exception('Unable to create share')
        except urllib2.HTTPError as e:
            error_message = e.read()
#             print error_message
            raise Exception('Unable to create share')


class ProjectShare(models.Model):
    project = models.OneToOneField(Project)
#     labshare = models.ForeignKey(LabShare)
    bioshare_id = models.CharField(max_length=15,null=True,blank=True)
#     folder = models.SlugField(max_length=50,unique=True)
#     class Meta:
#         unique_together = (('labshare','folder'),('project','labshare'))
    def save(self, *args, **kwargs):
        if not self.bioshare_id:
            if not os.path.exists(self.directory(full=True)):
                os.makedirs(self.directory(full=True))
            self.bioshare_id = self.project.group.bioshare_account.create_share('%s - %s'%(self.project.lab.name,self.project.name),self.directory())
        return super(ProjectShare, self).save(*args, **kwargs)
    def directory(self,full=True):
        return safe_join(self.project.directory(full=full),'share')
    #This should always return an empty array.  We don't want actual data, just a view on the data!
    def real_files(self,relpath=True,recalculate=False):
        if not hasattr(self, '_real_files') or recalculate: #only run once
            self._real_files = get_real_files(self.directory(full=True),relpath)
        return self._real_files
    def symlinks(self,relpath=True,recalculate=False):
        if not hasattr(self, '_symlinks') or recalculate: #only run once
            self._symlinks = get_symlinks(self.directory(full=True),relpath)
        return self._symlinks
    @property
    def url(self):
        return VIEW_URL.format(id=self.bioshare_id)
    def link_paths(self,paths):
        current_links = self.symlinks(relpath=True,recalculate=True)
        new_paths = list(set(remove_sub_paths(paths+current_links)) - set(current_links))
        ignored = list(set(paths) - set(new_paths))
        failed = []
        linked = []
        for path in new_paths:
            link_path = safe_join(self.directory(full=True),path)
            target_path = safe_join(self.project.directory(full=True),path)
            if os.path.exists(link_path) or os.path.lexists(link_path): #does the path exist as a symlink or otherwise?
                if os.path.isdir(link_path) and not os.path.islink(link_path):#if it is an empty directory (aside from symlinks and directories), delete it
                    if len(get_real_files(link_path))==0:
                        shutil.rmtree(link_path)
                    else:
                        failed.append(path)
                        continue
            parent_dir = os.path.abspath(os.path.join(link_path, os.pardir))
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
            os.symlink(target_path,link_path)
            linked.append(path)
        return {'linked':linked,'ignored':ignored,'failed':failed}
    def unlink_paths(self,paths):
        failed = []
        removed = []
        for path in paths:
            link_path = safe_join(self.directory(full=True),path)
            if os.path.lexists(link_path) and os.path.islink(link_path): #does the path exist as a symlink or otherwise?
                os.unlink(link_path)
                removed.append(path)
            else:
                failed.append(path)
        return {'removed':removed,'failed':failed}
    def set_paths(self,paths):
        current_links = self.symlinks(relpath=True,recalculate=True)
        remove_paths = list(set(current_links)-set(paths))
        remove_stats = self.unlink_paths(remove_paths)
        link_stats =self.link_paths(paths)
        return {'linked':link_stats['linked'],'ignored':link_stats['ignored'],'removed':remove_stats['removed'],'failed':remove_stats['failed']+link_stats['failed']}
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
    