from django.db import models
from django.contrib.auth.models import User
from glims.lims import Project
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.conf import settings

class BioinfoProject(models.Model):
    project = models.OneToOneField(Project)
    created = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User)
    description = models.TextField()

@receiver(post_save,sender=Project)
def create_bioinfo_project(sender,instance,**kwargs):
#     @todo: replace with non magic string
    print 'Create bioinfo project!!!!'
    if instance.status:
        if instance.status.id == 'BIOINFORMATICS':
            BioinfoProject.objects.get_or_create(project=instance)
