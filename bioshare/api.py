from rest_framework import viewsets, status
# from models import 
from bioshare.serializers import ProjectShareSerializer
from bioshare.models import ProjectShare
from glims.models import Project
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
        try:    
            project = Project.objects.get(id=request.data.get('project'))
    #         labshare, created = LabShare.objects.get_or_create(lab=project.lab,group=project.group) 
    #         data = {'project':request.data.get('project'),'folder':,'labshare':labshare.id}
            project_share = ProjectShare.objects.create(project=project)
            serializer = self.get_serializer(project_share)
    #         print "LABSHARE"
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception, e:
            return Response({'status':'error','message':e.message},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @detail_route(methods=['post'])
    def link_paths(self, request, pk=None):
        obj = self.get_object()
        paths = request.data.get('paths',[])
        stats = obj.link_paths(paths)
        return Response({'status': 'success','stats':stats,'symlinks':obj.symlinks(recalculate=True)})
#             return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    @detail_route(methods=['post'])
    def unlink_paths(self, request, pk=None):
        obj = self.get_object()
        paths = request.data.get('paths',[])
        stats = obj.unlink_paths(paths)
        return Response({'status': 'success','stats':stats,'symlinks':obj.symlinks(recalculate=True)})
    @detail_route(methods=['post'])
    def set_paths(self, request, pk=None):
        obj = self.get_object()
        paths = request.data.get('paths',[])
        stats = obj.set_paths(paths)
        return Response({'status': 'success','stats':stats,'symlinks':obj.symlinks(recalculate=True)})