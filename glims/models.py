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
from django.contrib.auth.models import Group, User
from django.core.validators import RegexValidator
from glims.settings import FILES_ROOT
from django.utils._os import safe_join
from django.utils.decorators import classproperty
from glims.files.utils import make_directory_name
from glims.signals.signals import directory_created
from glims.files.directories import call_directory_function

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
    first_name = models.CharField(max_length=30,null=True,blank=True,db_index=True)
    last_name = models.CharField(max_length=30,db_index=True)
    affiliation = models.CharField(max_length=50,choices=((affiliation,affiliation) for affiliation in settings.LAB_AFFILIATIONS),null=True,blank=True,db_index=True)
    description = models.TextField(db_index=True)
    url = models.URLField(blank=True,null=True)
    slug = models.SlugField(max_length=50,unique=True,null=True)
    @property
    def name(self):
        return '%s, %s'%(self.last_name,self.first_name) if self.first_name else self.last_name
    def get_directory_name(self):
        return call_directory_function('get_lab_directory_name',self)
#         parts = [self.last_name,self.first_name] if self.first_name else [self.last_name]
#         return make_directory_name('_'.join(parts))
    def get_group_directory(self,group,full=True):
        return call_directory_function('get_group_lab_directory',self,group,full=full)
#         path = os.path.join(make_directory_name(group.name),'labs',self.get_directory_name())#self.slug
#         if full:
#             path = safe_join(FILES_ROOT,path)
#         return path
    def __unicode__(self):
        return self.name

class Project(ExtensibleModel):
    project_id = models.CharField(max_length=4,default=generate_project_id,unique=True,null=True,blank=True,db_index=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    lab = models.ForeignKey(Lab, on_delete=models.PROTECT,related_name='projects')
    name = models.CharField(max_length=100,db_index=True)
    description = models.TextField(null=True,blank=True,db_index=True)
    contact = models.TextField(null=True,blank=True)
    sample_type = models.ForeignKey(ModelType, null=True, blank=True, limit_choices_to = {'content_type__model':'sample'}, related_name="+",on_delete=models.PROTECT)
    status = models.ForeignKey('Status',null=True,blank=True, on_delete=models.PROTECT)
    manager = models.ForeignKey(User,null=True,blank=True,related_name='+',on_delete=models.PROTECT)
    participants = models.ManyToManyField(User,related_name='+')
    related_projects = models.ManyToManyField('self')
    archived = models.BooleanField(default=False)
    history = JSONField(null=True,blank=True,default={})
    def directory(self,full=True):
        return call_directory_function('get_project_directory',self,full=full)
#         path =  os.path.join(self.lab.get_group_directory(self.group,full=full),'projects','ID',self.project_id)
#         return path
    def symlink_path(self,full=True):
        return os.path.join(self.lab.get_group_directory(self.group,full=full),'projects','NAME',self.get_directory_name())
    def create_directories(self):
        return call_directory_function('create_project_directories',self) 
#         dir = self.directory(full=True)
#         symlink = self.symlink_path(full=True)
#         symlink_directory = os.path.normpath(os.path.join(symlink,'../'))
#         if not os.path.exists(symlink_directory):
#             os.makedirs(symlink_directory)
#     #     os.unlink(alias_dir)
#         if not os.path.exists(dir):
#             os.makedirs(dir)
#             directory_created.send(sender=self.__class__,instance=self, directory=dir)
#         if not os.path.lexists(symlink):
#             target = '../ID/{0}'.format(self.project_id)
#             os.symlink(target,symlink)
    def statuses(self):
        return Status.objects.filter(model_type=self.model_type).order_by('order')
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('project', args=[str(self.id)])
    def get_group(self):
        return self.group
    def get_directory_name(self):
        return make_directory_name(self.name)
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


class Sample(ExtensibleModel):
    sample_id = models.CharField(max_length=60,unique=True,null=True,blank=True)
    project = models.ForeignKey(Project, related_name="samples",null=True,blank=True)
    name = models.CharField(max_length=100,db_index=True)
    description = models.TextField(null=True,blank=True,db_index=True)
    created = models.DateTimeField(auto_now=True,db_index=True)
    received = models.DateField(null=True,blank=True,db_index=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('sample', args=[str(self.id)])
    def directory(self,full=True):
        return call_directory_function('get_sample_directory',self,full=full)
#         dir = self.sample_id
#         if self.name:
#             dir = make_directory_name(self.name)
#         return  os.path.join(self.project.directory(full=full),'samples',dir)
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

class Adapter(ExtensibleModel):
    name = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)

class Library(ExtensibleModel):
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    name = models.CharField(max_length=100,null=True,blank=True,db_index=True)
    sample = models.ForeignKey(Sample,related_name='libraries')
    adapter = models.ForeignKey(Adapter,null=True,blank=True,related_name='libraries')
    description = models.TextField(null=True,blank=True,db_index=True)
    def get_group(self):
        try:
            return self.sample.project.group
        except:
            return None
    def __unicode__(self):
        return self.name

class Pool(ExtensibleModel):
    name = models.CharField(max_length=100,unique=True,db_index=True)
    group = models.ForeignKey(Group,on_delete=models.PROTECT)
    description = models.TextField(null=True,blank=True,db_index=True)
    created = models.DateField(auto_now=True,db_index=True)
    libraries = models.ManyToManyField(Library,related_name='pools')
    library_data = JSONField(null=True,blank=True,default={})
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('pool', args=[str(self.id)])
    def get_group(self):
        return self.group
    @staticmethod
    def user_queryset(user):
        Pool.objects.filter(group__in=user.groups)
    def get_barcode_duplicates(self):
        barcodes = self.get_library_barcodes()
        duplicates = {barcode:libraries for barcode,libraries in barcodes.iteritems() if len(libraries) > 1}
        return duplicates if len(duplicates) > 0 else None
    def get_library_barcodes(self):
        barcodes = {}
        for l in self.libraries.select_related('adapter').filter(adapter__isnull=False):
            if not barcodes.has_key(l.adapter.barcode):
                barcodes[l.adapter.barcode] = []
            barcodes[l.adapter.barcode].append(l.name)
        return barcodes

class Status(models.Model):
    model_type = models.ForeignKey(ModelType,related_name="status_options")
    name = models.CharField(max_length=30,db_index=True)
    description = models.TextField(null=True,blank=True,db_index=True)
    order = models.PositiveSmallIntegerField()
    def __unicode__(self):
        return self.name

class EmailTemplate(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=250)
    body = models.TextField()

class Email(models.Model):
    created = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=250)
    body = models.TextField()
    def serialize(self):
        sent = self.recipients.filter(sent__isnull=False).count()
        unsent = self.recipients.filter(sent__isnull=True).count()
        return {'created':self.created,'subject':self.subject,'body':self.body,'sent':sent,'unsent':unsent}
    @classmethod
    def create_from_template(cls, template, to_addresses):
        return cls.create(template.subject, template.body, to_addresses)
    @classmethod
    def create(cls, subject, body, to_addresses):
        email = cls(subject=subject, body=body)
        email.save()
        for address in to_addresses:
            EmailRecipient(email=email,address=address).save()
        return email
    def send(self,context={}):
        from django.core.mail import send_mail
        from datetime import datetime
        from django.template import Context, Template
        for er in self.recipients.filter(sent__isnull=True):
            try:
                try:
                    user = User.objects.get(email=er.address)
                    user_context = {'user':user}
                    user_context.update(context)
                    c = Context(user_context)
                except Exception, e:
                    c = Context(context)
                subject_template = Template(self.subject)
                body_template = Template(self.body)
                send_mail(subject_template.render(c), body_template.render(c), settings.ADMIN_EMAIL, ['amschaal@gmail.com'], fail_silently=False)
                er.sent = datetime.now()
                er.save()
            except Exception, e:
                print e
class EmailRecipient(models.Model):
    email = models.ForeignKey(Email,related_name='recipients')
    address = models.CharField(max_length=75)
    sent = models.DateTimeField(auto_now=False, null=True, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,related_name='profile')
    group = models.ForeignKey(Group,null=True,blank=True)
    preferences = JSONField(default=dict)

def user_name(self):
    return "%s %s" % (self.first_name, self.last_name)
User.name = property(user_name)
