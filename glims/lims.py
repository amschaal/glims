from django.db import models
from django.contrib.auth.models import Group, User
from uuid import uuid4
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import Q
from models import Plugin
import operator
'''
Contains base structure for LIMS components

Permissions are inherited from owner->project->project->sample (start at sample level until you get to owner)


PI (Billing system)
-------------------
name
type (PI, Company, etc)
assign_permissions(permissions=[],users=[])
revoke_permissions(permissions=[],users=[])


Project (Abstract)
------------------
PI (references User)
name
assign_permissions(permissions=[],users=[])
revoke_permissions(permissions=[],users=[])


Maybe not needed: Project (Abstract)
------------------
project
name
assign_permissions(permissions=[],users=[])
revoke_permissions(permissions=[],users=[])


Sample (Abstract)
-----------------
project
assign_permissions(permissions=[],users=[])
revoke_permissions(permissions=[],users=[])

Experiment (Abstract)
------------------
sample
name
assign_permissions(permissions=[],users=[])
revoke_permissions(permissions=[],users=[])


'''
def generate_pk():
    return str(uuid4())[:20]

class ProjectType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    plugins = models.ManyToManyField(Plugin,null=True,blank=True)
    def __unicode__(self):
        return self.name

class Project(models.Model):
    id = models.CharField(max_length=20,unique=True,primary_key=True,default=generate_pk)
    type = models.ForeignKey(ProjectType)
    group = models.ForeignKey(Group)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
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

class Sample(models.Model):
    sample_id = models.CharField(max_length=30,unique=True)
    project = models.ForeignKey(Project, related_name="samples")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
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
    @staticmethod
    def get_all_objects(model_pks={}):
        queries = []
        for model, pks in model_pks.items():
            if model == 'Sample':
                queries.append(Q(pk__in = pks))
            if model == 'Project':
                queries.append(Q(project__pk__in = pks))
        return Sample.objects.filter(reduce(operator.or_, queries))
    
        

    
class Experiment(models.Model):
    id = models.CharField(max_length=30,unique=True,primary_key=True,default=generate_pk)
    sample = models.ForeignKey(Sample, related_name="experiments")
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('experiment', args=[str(self.id)])
    class Meta:
        app_label = 'glims'
        permissions = (
            ('view', 'View Experiment'),
            ('admin', 'Administer Experiment'),
        )
    def inherit_from(self):
        return [self.sample,self.sample.project]
    inherited_classes = [Project,Sample]
    @staticmethod
    def get_all_objects(model_pks={}):
        queries = []
        for model, pks in model_pks.items():
            if model == 'Experiment':
                queries.append(Q(pk__in = pks))
            if model == 'Sample':
                queries.append(Q(sample__pk__in = pks))
            if model == 'Project':
                queries.append(Q(sample__project__pk__in = pks))
        return Experiment.objects.filter(reduce(operator.or_, queries))
    
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