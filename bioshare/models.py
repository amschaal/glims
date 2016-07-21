from django.db import models
from glims.lims import Lab
from django.contrib.auth.models import Group
from django.utils._os import safe_join

class BioshareAccount(models.Model):
    group = models.OneToOneField(Group, related_name="bioshare_account")
    auth_token = models.CharField(max_length=100)

class LabShare(models.Model):
    lab = models.ForeignKey(Lab)
    group = models.ForeignKey(Group)
    bioshare_id = models.CharField(max_length=10)
    class Meta:
        unique_together = (('lab','group'))
    @property
    def directory(self):
        return safe_join(self.group.name.replace(' ','_'),'labs',self.lab.slug,'share')

class ProjectShare(models.Model):
    labshare = models.ForeignKey(LabShare)
    folder = models.CharField(max_length=50)
    class Meta:
        unique_together = (('labshare','folder'))
    @property
    def directory(self):
        return safe_join(self.labshare.directory,self.folder)
    