from django.db import models
from django.contrib.auth.models import Group, User
from uuid import uuid4
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import Q
from models import Plugin
from jsonfield import JSONField
from django_json_forms.models import JSONFormModel
from extensible.models import ModelType, ExtensibleModel
import operator, os
from django.conf import settings
from math import floor
import string
import random
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver

from django.db import transaction
from django_cloudstore.models import CloudStore
from django_cloudstore.engines.bioshare import BioshareStorageEngine

def generate_pk():
    return str(uuid4())[:15]
def generate_project_id(size=3, chars=string.ascii_uppercase + string.digits):
    for _ in range (10):
        id = ''.join(random.choice(chars) for _ in range(size))
        if not Project.objects.filter(project_id=id).exists():
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

# class ModelType(models.Model):
#     content_type = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     plugins = models.ManyToManyField(Plugin,null=True,blank=True, through='ModelTypePlugins')
#     schema = JSONField(null=True,blank=True)
# #     form_model = models.ForeignKey(JSONFormModel,null=True,blank=True)
#     def __unicode__(self):
#         return "%s: %s" % (self.content_type, self.name)
# #   *fields - A postgres json field
# #       Contains the field definitions for custom model attributes
# ModelType.plugins = models.ManyToManyField(Plugin,null=True,blank=True, through='ModelTypePlugins')

class ModelTypePlugins(models.Model):
    INLINE_LAYOUT = 'inline'
    TABBED_LAYOUT = 'tabbed'
    LAYOUTS = ((INLINE_LAYOUT,'Inline'),(TABBED_LAYOUT,'Tab'))
    type = models.ForeignKey(ModelType)
    plugin = models.ForeignKey(Plugin)
    weight = models.IntegerField(default=0)
    layout = models.CharField(max_length=10,choices=LAYOUTS)
    header = models.CharField(max_length=30, null=True, blank=True)

# class ExtensibleModel(models.Model):
# #     id = models.CharField(max_length=30,primary_key=True,default=generate_pk)
#     type = models.ForeignKey(ModelType, null=True, blank=True)
#     data = JSONField(null=True,blank=True,default={})
#     #@deprecated: will use json, eventually will use native jsonb field with Django 1.9
# #     data = hstore.DictionaryField(null=True)#schema=get_schema
# #     refs = hstore.ReferencesField()
# #     objects = hstore.HStoreManager()
#     class Meta:
#         abstract = True

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
# class ProjectType(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(null=True,blank=True)
#     plugins = models.ManyToManyField(Plugin,null=True,blank=True, through='ProjectTypePlugins')
#     def __unicode__(self):
#         return self.name
#     class Meta:
#         app_label = 'glims'


# class ProjectTypePlugins(models.Model):
#     INLINE_LAYOUT = 'inline'
#     TABBED_LAYOUT = 'tabbed'
#     LAYOUTS = ((INLINE_LAYOUT,'Inline'),(TABBED_LAYOUT,'Tab'))
#     type = models.ForeignKey(ProjectType)
#     plugin = models.ForeignKey(Plugin)
#     weight = models.IntegerField(default=0)
#     layout = models.CharField(max_length=10,choices=LAYOUTS)
#     header = models.CharField(max_length=30, null=True, blank=True)
#     class Meta:
#         app_label = 'glims'
# class Filesystem(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField()
#     path = models.CharField(max_length=200)
#     archive_path = models.CharField(max_length=200)
#     users = models.ManyToManyField(User, related_name='filesystems')
#     def __unicode__(self):
#         return '%s: %s' %(self.name, self.path)
class Lab(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=20,unique=True,null=True)
    cloudstore = models.ForeignKey(CloudStore,null=True,blank=True,on_delete=models.SET_NULL)
    def create_cloudstore(self):
        if not self.cloudstore:
            self.cloudstore = BioshareStorageEngine.create(self.name, self.description, {'link_to_path':self.directory})
            self.save()
#     def get_absolute_url(self):
#         return reverse('lab', args=[str(self.id)])
    @property
    def directory(self):
        return os.path.join(settings.LAB_DATA_DIRECTORY,self.slug)
    def create_directory(self):
        if self.slug:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory, mode=0774)
    def __unicode__(self):
        return self.name

class Project(ExtensibleModel):
    project_id = models.CharField(max_length=4,default=generate_project_id,unique=True,null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    lab = models.ForeignKey(Lab)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    sample_type = models.ForeignKey(ModelType, null=True, blank=True, limit_choices_to = {'content_type__model':'sample'}, related_name="+")
#     sub_directory = models.CharField(max_length=50,null=True,blank=True)
    @property
    def directory(self):
        return os.path.join(self.lab.directory,self.project_id)
    def create_directory(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, mode=0774)
    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs) # Call the "real" save() method.
        self.create_directory()
#     def limit_sample_type_choices(self):
#         return {'content_type_id': 16}
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('project', args=[str(self.id)])
    class Meta:
        app_label = 'glims'
        permissions = (
            ('view', 'View Project'),
            ('admin', 'Administer Project'),
            ('pi', 'Can PI a Project'),
        )

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
    class Meta:
        app_label = 'glims'
        permissions = (
            ('view', 'View Sample'),
            ('admin', 'Administer Sample'),
        )
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

    
# class ProcessTemplate(models.Model):
#     type = models.ForeignKey(ModelType)
#     name = models.CharField(max_length=100)
#     description = models.TextField(null=True,blank=True)


class Pool(ExtensibleModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    created = models.DateField(auto_now=True)
    samples = models.ManyToManyField(Sample,related_name='pools')
    sample_data = JSONField(null=True,blank=True,default={})
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('pool', args=[str(self.id)])

class WorkflowTemplate(models.Model):
    type = models.ForeignKey(ModelType,related_name='+')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    processes = models.ManyToManyField(ModelType,through="WorkflowProcess",related_name='+')
    def __unicode__(self):
        return self.name

class WorkflowProcess(models.Model):
    workflow = models.ForeignKey(WorkflowTemplate)
    process = models.ForeignKey(ModelType,related_name='+')
    order = models.IntegerField()

class Workflow(ExtensibleModel):
    samples = models.ManyToManyField(Sample)
    pool = models.ForeignKey(Pool,null=True,blank=True)
    workflow_template = models.ForeignKey(WorkflowTemplate)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    created = models.DateField(auto_now=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('workflow', args=[str(self.id)])

class Process(ExtensibleModel):
    workflow = models.ForeignKey(Workflow, related_name="processes")
#     workflow_process = models.ForeignKey(WorkflowProcess,related_name='+')
    sample_data = JSONField(null=True,blank=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('process', args=[str(self.id)])


# Attach a file to just about anything:
# file = File(text='My wonderful note',created_by=request.user,content_object=some_model_instance)
# file.save()
# class File(models.Model):
#     file = models.FileField(upload_to='files')
#     name = models.CharField(max_length=100)
#     description = models.TextField(null=True,blank=True)
#     uploaded_by = models.ForeignKey(User,null=True,blank=True)
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.CharField(max_length=30) #Can be coerced into integer key if necessary
#     content_object = GenericForeignKey('content_type', 'object_id')
#     admin_only = models.BooleanField(default=True)
#     
#     class Meta:
#         app_label = 'glims'
#     def __unicode__(self):              # __unicode__ on Python 2
#         return self.file.name[:30]+'...'
#     
# class Note(models.Model):
#     parent = models.ForeignKey('Note',null=True,blank=True)
#     content = models.TextField()
#     created_by = models.ForeignKey(User,null=True,blank=True, related_name='notes')
#     created = models.DateTimeField(auto_now=True)
#     modified_by = models.ForeignKey(User,null=True,blank=True, related_name='+')
#     modified = models.DateTimeField(auto_now=True)
#     content_type = models.ForeignKey(ContentType)
#     object_id = models.CharField(max_length=30) #Can be coerced into integer key if necessary
#     content_object = GenericForeignKey('content_type', 'object_id')
#     admin_only = models.BooleanField(default=True)
#     class Meta:
#         app_label = 'glims'
#     def __unicode__(self):              # __unicode__ on Python 2
#         return self.content[:50]+'...'