from django.db import models
from django.contrib.auth.models import User
from glims.lims import Project
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

class BioinfoProject(models.Model):
    name = models.CharField(max_length=100)
#     type = models.CharField(max_length=20,choices=[])
    project = models.OneToOneField(Project)
    created = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(User,null=True,blank=True,related_name='+')
    participants = models.ManyToManyField(User,related_name='+')
    description = models.TextField(null=True,blank=True)

@receiver(post_save,sender=Project)
def create_bioinfo_project(sender,instance,**kwargs):
#     @todo: replace with non magic string
    print 'Create bioinfo project!!!!'
    if instance.status:
        if instance.status.id == 'BIOINFORMATICS':
            BioinfoProject.objects.get_or_create(project=instance)