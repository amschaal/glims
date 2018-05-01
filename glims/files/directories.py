import os
from django.conf import settings
from django.utils.module_loading import import_string
from glims.files.utils import make_directory_name
from django.utils._os import safe_join

def call_directory_function(function_name,*args,**kwargs):
    func = import_string(settings.DIRECTORY_FUNCTIONS.get(function_name))
    return func(*args,**kwargs)

#Project directory functions below

def get_project_directory(project,full=True):
    return os.path.join(project.lab.get_group_directory(project.group,full=full),'projects','ID',project.project_id)

def create_project_directories(project):
    dir = project.directory(full=True)
    symlink = project.symlink_path(full=True)
    symlink_directory = os.path.normpath(os.path.join(symlink,'../'))
    if not os.path.exists(symlink_directory):
        os.makedirs(symlink_directory)
#     os.unlink(alias_dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
#         directory_created.send(sender=self.__class__,instance=self, directory=dir)
    if not os.path.lexists(symlink):
        target = '../ID/{0}'.format(project.project_id)
        os.symlink(target,symlink)

#Lab directory functions below

def get_lab_directory_name(lab):
    return lab.slug
#     parts = [lab.last_name,lab.first_name] if lab.first_name else [lab.last_name]
#     return make_directory_name('_'.join(parts))

def get_group_lab_directory(lab,group,full=True):
    path = os.path.join(make_directory_name(group.name),'labs',lab.get_directory_name())#self.slug
    if full:
        path = safe_join(settings.FILES_ROOT,path)
    return path
 
# Sample directory functions below

def get_sample_directory(sample,full=True):
    dir = sample.sample_id
    if sample.name:
        dir = make_directory_name(sample.name)
    return  os.path.join(sample.project.directory(full=full),'samples',dir) 