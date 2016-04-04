from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
from proteomics.utils import count_sequences, create_reverse
from django.conf import settings
import subprocess
from django.forms.models import fields_for_model
class FastaFile(models.Model):
#     FORWARD = 'forward'
#     REVERSE = 'reverse'
#     FORWARD_AND_REVERSE = 'forward_and_reverse'
#     TYPE_CHOICES = ((FORWARD,'Forward'),(REVERSE,'Reverse'),(FORWARD_AND_REVERSE,'Forward and Reverse'))
#     parent = models.ForeignKey('self',null=True)
    file = models.FileField(upload_to='fasta_files',blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
#     type = models.CharField(max_length=20,choices=TYPE_CHOICES)
    modified = models.DateField(null=True)
    count = models.IntegerField(null=True)
    uploaded_by = models.ForeignKey(User,null=True,blank=True)
    #@todo: Add function to create Reverse, Forward w/ Crap, F+R w/ Crap
    def create_decoys(self):
        #Should be doing this to F+R w/ Crap
        if self.file:
            return subprocess.call(['java','-cp', settings.SEARCHGUI_PATH, 'eu.isas.searchgui.cmd.FastaCLI', '-in', self.file.path, '-decoy'])
    def __unicode__(self):              # __unicode__ on Python 2
        return self.name
@receiver(post_delete, sender=FastaFile)
def delete_fastafile(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(False)
@receiver(post_save, sender=FastaFile)
def save_fastafile(sender, instance, **kwargs):
    if kwargs['created']:
        if instance.file:
            instance.count = count_sequences(instance.file)
#         print create_reverse(instance)
@receiver(post_save, sender=FastaFile)
def run_fastacli(sender, instance, created, **kwargs):
    instance.create_decoys()

class ParameterFile(models.Model):
    file = models.FileField(upload_to='compomics_parameter_files')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    uploaded_by = models.ForeignKey(User,null=True,blank=True)
    def __unicode__(self):              # __unicode__ on Python 2
        return self.name
@receiver(post_delete, sender=ParameterFile)
def delete_parameterfile(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(False)

"""
Sample fields:



"""
