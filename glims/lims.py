from django.db import models
from uuid import uuid4
from django.core.urlresolvers import reverse
from django.db.models import Q
from jsonfield import JSONField
from extensible.models import ModelType, ExtensibleModel
import operator, os
from django.conf import settings
import string
import random
from django.db import transaction
from glims.models import Status
from django.contrib.auth.models import Group, User
from django.core.validators import RegexValidator
from glims.settings import FILES_ROOT
from django.utils.text import slugify
from django.utils._os import safe_join

def generate_pk():
    return str(uuid4())[:15]
def generate_project_id(size=3, chars=string.ascii_uppercase + string.digits):
    try:
        for _ in range (10):
            id = ''.join(random.choice(chars) for _ in range(size))
            if not Project.objects.filter(project_id=id).exists():
                return id
    except:
        return id
#A01-A99,B01-B99, etc
def generate_sample_id(project):#last_id='A00'
    last = Sample.objects.filter(project=project,sample_id__regex=r'^[A-Z0-9]{3}[A-Z]\d{2}').last()
    last_id = 'A00' if not last else last.sample_id[-3:]
    alphanumeric = map(chr,range(65,91))#range(48,57)+
    value = alphanumeric.index(last_id[0])*99 + int(last_id[1:3]) + 1
    prefix =  string.ascii_uppercase[int(value / 100)]
    suffix = str((value%99)).zfill(2)
    return "%s%s" % (project.project_id,prefix+suffix)


file_directory_validator = RegexValidator(r'^[0-9a-zA-Z_]*$','Directories should only contain alphanumeric characters and underscores.')

"""
        
class MyModel(ExtensibleModel)
    name = models.CharField(max_length=50)
#https://docs.djangoproject.com/en/1.7/topics/db/models/#proxy-models    
class MyModelExtended(MyModel):
    class Meta:
        proxy = True
    def ref_field_options(self,field_name):
        if field_name == 'run':
            return Run.objects.filter(foo=bar).values('id','name')
        ...
"""
class Lab(models.Model):
    name = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=20,choices=((affiliation,affiliation) for affiliation in settings.LAB_AFFILIATIONS),null=True,blank=True)
    description = models.TextField()
    url = models.URLField(blank=True,null=True)
    slug = models.SlugField(max_length=20,unique=True,null=True)
    def __unicode__(self):
        return self.name

class Project(ExtensibleModel):
    project_id = models.CharField(max_length=4,default=generate_project_id,unique=True,null=True,blank=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    lab = models.ForeignKey(Lab, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    sample_type = models.ForeignKey(ModelType, null=True, blank=True, limit_choices_to = {'content_type__model':'sample'}, related_name="+",on_delete=models.PROTECT)
    status = models.ForeignKey(Status,null=True,blank=True, on_delete=models.PROTECT)
    manager = models.ForeignKey(User,null=True,blank=True,related_name='+',on_delete=models.PROTECT)
    participants = models.ManyToManyField(User,related_name='+')
    related_projects = models.ManyToManyField('self')
    archived = models.BooleanField(default=False)
    history = JSONField(null=True,blank=True,default={})
    def directory(self,full=True):
        path =  os.path.join(self.group.name.replace(' ','_'),'labs',self.lab.slug,'projects','ID',self.project_id)
        if full:
            path = safe_join(FILES_ROOT,path)
        return path
    @property
    def symlink_path(self):
        return '{0}/labs/{1}/projects/NAME/{2}'.format(self.group.name.replace(' ','_'),self.lab.slug,self.name.replace(' ','_'))
    def create_directories(self):
        dir = self.directory(full=True)
        symlink = os.path.join(FILES_ROOT,self.symlink_path)
        symlink_directory = os.path.normpath(os.path.join(symlink,'../'))
        if not os.path.exists(symlink_directory):
            os.makedirs(symlink_directory)
    #     os.unlink(alias_dir)
        if not os.path.exists(dir):
            os.makedirs(dir)
        if not os.path.lexists(symlink):
            target = '../ID/{0}'.format(self.project_id)
            os.symlink(target,symlink)
    def statuses(self):
        return Status.objects.filter(model_type=self.model_type).order_by('order')
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('project', args=[str(self.id)])
    def get_group(self):
        return self.group
    def slugify_name(self):
        return slugify(self.name.replace(' ','_'))
    @staticmethod
    def user_queryset(user):
        Project.objects.filter(group__in=user.groups)
    class Meta:
        app_label = 'glims'
        permissions = (
            ('view', 'View Project'),
            ('admin', 'Administer Project'),
            ('pi', 'Can PI a Project'),
        )
#         unique_together = (('lab','file_directory'),)

# class ProjectStatus(models.Model):
#     project = models.ForeignKey(Project,related_name="statuses")
#     status = models.ForeignKey(Status)
#     set_by = models.ForeignKey(User)
#     timestamp = models.DateTimeField(auto_now=True)

class Sample(ExtensibleModel):
    sample_id = models.CharField(max_length=60,unique=True)
    project = models.ForeignKey(Project, related_name="samples",null=True,blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    received = models.DateField(null=True,blank=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('sample', args=[str(self.id)])
    def directory(self,full=True):
        dir = self.sample_id
        if self.name:
            dir = self.name.replace(' ','_')
        return  os.path.join(self.project.directory(full=full),'samples',dir)
    def get_group(self):
        if not self.project:
            return None
        return self.project.group
    @staticmethod
    def user_queryset(user):
        Sample.objects.filter(project__group__in=user.groups)
    class Meta:
        app_label = 'glims'
        permissions = (
            ('view', 'View Sample'),
            ('admin', 'Administer Sample'),
        )
        unique_together = (('sample_id','project'),('name','project'),)
    def inherit_from(self):
        return [self.project]
    inherited_classes = [Project]
    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.id:
#             if not self.sample_id and self.project:
#             last = Sample.objects.filter(project=self.project,sample_id__regex=r'^[A-Z]\d{2}').last()
            sample_id = generate_sample_id(self.project)
            self.sample_id = sample_id
        super(Sample, self).save(*args, **kwargs)
    @staticmethod
    def get_all_objects(model_pks={}):
        queries = []
        for model, pks in model_pks.items():
            if model == 'Sample':
                queries.append(Q(pk__in = pks))
            if model == 'Project':
                queries.append(Q(project__pk__in = pks))
        return Sample.objects.filter(reduce(operator.or_, queries))

class Pool(ExtensibleModel):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group,on_delete=models.PROTECT)
    description = models.TextField(null=True,blank=True)
    created = models.DateField(auto_now=True)
    samples = models.ManyToManyField(Sample,related_name='pools',null=True,blank=True)
    sample_data = JSONField(null=True,blank=True,default={})
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('pool', args=[str(self.id)])
    def get_group(self):
        return self.group
    @staticmethod
    def user_queryset(user):
        Pool.objects.filter(group__in=user.groups)
