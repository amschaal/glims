from glims.signals.signals import directory_created
from glims.models import Project
from django.dispatch.dispatcher import receiver
import os

@receiver(directory_created,sender=Project)
def create_project_afs_volume(sender,instance,directory,**kwargs):
    vol_name = "%s-deliverables"%instance.project_id
    deliverables_directory = os.path.join(directory,'deliverables')
    print "vos create -server foo.genomecenter.ucdavis.edu -partition bar -name '%s'"%vol_name
    print "fs mkm -vol %s -dir %s" % (vol_name,deliverables_directory)
    print "****SETUP AUTH****"
    print "fs sa %s BIOSHARE rl" % directory #give bioshare access read only access to whole project
    print "fs sa %s <LAB_GROUP> rl" % deliverables_directory #give lab group read only access to deliverables
