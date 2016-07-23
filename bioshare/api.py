from rest_framework import viewsets, status
# from models import 
from bioshare.serializers import ProjectShareSerializer
from bioshare.models import ProjectShare, LabShare
from glims.lims import Project
from rest_framework.response import Response
from glims.api.mixins import FileBrowserMixin, FileDownloadMixin
from bioshare.utils import remove_sub_paths
from rest_framework.decorators import detail_route
from django.utils._os import safe_join
import os
from os.path import exists
from os import makedirs

class ProjectShareViewSet(viewsets.ModelViewSet,FileBrowserMixin,FileDownloadMixin):
    serializer_class = ProjectShareSerializer
    model = ProjectShare
    filter_fields = ('project',)
    queryset = ProjectShare.objects.all()
#     def create(self, request, *args, **kwargs):
#         return viewsets.ModelViewSet.create(self, request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=request.data.get('project'))
        labshare, created = LabShare.objects.get_or_create(lab=project.lab,group=project.group) 
#         data = {'project':request.data.get('project'),'folder':,'labshare':labshare.id}
        project_share = ProjectShare.objects.create(project=project,labshare=labshare,folder=request.data.get('directory',project.slugify_name()))
        serializer = self.get_serializer(project_share)
#         print "LABSHARE"
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    @detail_route(methods=['post'])
    def link_paths(self, request, pk=None):
        obj = self.get_object()
        paths = request.data.get('paths',[])
        pruned_paths = remove_sub_paths(paths)
        for path in pruned_paths:
            link_path = safe_join(obj.directory(full=True),path)
            target_path = safe_join(obj.project.directory(),path)
            if not os.path.exists(link_path):
                if os.path.islink(link_path):
                    os.unlink(link_path)
                parent_dir = os.path.abspath(os.path.join(link_path, os.pardir))
                if not os.path.exists(parent_dir):
                    os.makedirs(parent_dir)
                os.symlink(target_path,link_path)
        return Response({'status': 'success','paths':pruned_paths})
#             return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)