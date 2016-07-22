from rest_framework import viewsets, status
# from models import 
from bioshare.serializers import ProjectShareSerializer
from bioshare.models import ProjectShare, LabShare
from glims.lims import Project
from rest_framework.response import Response

class ProjectShareViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectShareSerializer
    model = ProjectShare
    filter_fields = ('project',)
    queryset = ProjectShare.objects.all()
#     def create(self, request, *args, **kwargs):
#         return viewsets.ModelViewSet.create(self, request, *args, **kwargs)
    def create(self, request, *args, **kwargs):
        project = Project.objects.get(id=request.POST.get('project'))
        labshare, created = LabShare.objects.get_or_create(lab=project.lab,group=project.group) 
#         data = {'project':request.data.get('project'),'folder':,'labshare':labshare.id}
        project_share = ProjectShare.objects.create(project=project,labshare=labshare,folder=request.data.get('directory',project.name.replace(' ','_')))
        serializer = self.get_serializer(project_share)
#         print "LABSHARE"
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)