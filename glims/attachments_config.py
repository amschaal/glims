def attachment_upload_to(instance, filename):
    from glims.lims import Project, Sample
    obj = instance.content_object
    if isinstance(obj, Project):
        return '{0}/labs/{1}/projects/{2}/files/{3}'.format(obj.group.name,obj.lab.slug,obj.project_id, filename)
    if isinstance(obj, Sample):
        return '{0}/labs/{1}/projects/{2}/samples/{3}/files/{4}'.format(obj.project.group.name,obj.project.lab.slug,obj.project.project_id,obj.sample_id, filename)
    else:
        return 'files/{1}'.format(filename)