import os

def create_project_directories(project):
    dir = project.directory(full=True)
    symlink = project.symlink_path(full=True)
    symlink_directory = os.path.normpath(os.path.join(symlink,'../'))
    if not os.path.exists(symlink_directory):
        os.makedirs(symlink_directory)
#     os.unlink(alias_dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
        vol_name = "%s-deliverables"%project.project_id
        deliverables_directory = os.path.join(dir,'deliverables')
        print "vos create -server foo.genomecenter.ucdavis.edu -partition bar -name '%s'"%vol_name
        print "fs mkm -vol %s -dir %s" % (vol_name,deliverables_directory)
        print "****SETUP AUTH****"
        print "fs sa %s BIOSHARE rl" % dir #give bioshare access read only access to whole project
        print "fs sa %s <LAB_GROUP> rl" % deliverables_directory #give lab group read only access to deliverables

#         directory_created.send(sender=self.__class__,instance=self, directory=dir)
    if not os.path.lexists(symlink):
        target = '../ID/{0}'.format(project.project_id)
        os.symlink(target,symlink)