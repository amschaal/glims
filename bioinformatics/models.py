from django.db import models
from django.contrib.auth.models import User
from glims.lims import Project, Lab
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from extensible.models import ExtensibleModel
from glims.models import Status
from attachments.models import delete_attachments
from django.core.urlresolvers import reverse

class BioinfoProject(ExtensibleModel):
    name = models.CharField(max_length=100)
#     type = models.CharField(max_length=20,choices=[])
    status = models.ForeignKey(Status,blank=True,null=True)
    project = models.OneToOneField(Project,blank=True,null=True,related_name='bioinfo_project')
    lab = models.ForeignKey(Lab,related_name="bioinfo_projects",blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    manager = models.ForeignKey(User,null=True,blank=True,related_name='+')
    participants = models.ManyToManyField(User,related_name='+')
    description = models.TextField(null=True,blank=True)
    data_location = models.CharField(max_length=250,blank=True,null=True)
    def get_absolute_url(self):
        return reverse('bioinformatics__project', args=[str(self.id)])
    def get_notification_users(self):
        return self.participants.all() | User.objects.filter(id=self.manager_id)

@receiver(post_save,sender=Project)
def create_bioinfo_project(sender,instance,**kwargs):
#     @todo: replace with non magic string
    print 'Create bioinfo project!!!!'
    if instance.status:
        if instance.status.id == 'BIOINFORMATICS':
            BioinfoProject.objects.get_or_create(project=instance)

post_delete.connect(delete_attachments, sender=BioinfoProject)
