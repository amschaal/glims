import os
def attachment_upload_to(instance, filename):
#     from glims.lims import Project, Sample
    obj = instance.content_object
    if hasattr(obj, 'directory'):
        return os.path.join(obj.directory(full=False),'uploads',filename)
    else:
        return 'files/{0}/{1}/{2}'.format(obj.__class__.__name__,obj.id,filename)