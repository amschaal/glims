from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONPRenderer, JSONRenderer
from glims.models import JobFactory
from glims.lims import Study, Sample, Experiment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from permissions.manage import get_all_user_objects, has_all_permissions
# from models import 
from django.core.exceptions import ObjectDoesNotExist
from glims.serializers import *
from rest_framework import filters


class CustomPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:            
            return True

        # Instance must have an attribute named `owner`.
        return has_all_permissions(request.user, obj, ['admin'])


@api_view(['POST'])
# @permission_classes((ServerAuth, ))  
def update_job(request, job_id):
    status = request.DATA.get('status')
    job = JobFactory.get_job(job_id)
    job.update_status(status)
    return Response({})


# class StudyViewset(viewsets.ViewSet):
#     queryset = Study.objects.all()
#     """
#     A simple ViewSet that for listing or retrieving studies.
#     """
#     def list(self, request):
#         queryset = get_all_user_objects(request.user, ['view'], Study)
#         serializer = StudySerializer(queryset, many=True)
#         return Response(serializer.data)
#     def retrieve(self, request, pk=None):
#         queryset = get_all_user_objects(request.user, ['view'], Study)
#         study = get_object_or_404(queryset, pk=pk)
#         serializer = StudySerializer(study)
#         return Response(serializer.data)

class StudyViewSet(viewsets.ModelViewSet):
    serializer_class = StudySerializer
    permission_classes = [CustomPermission]
    model = Study
    filter_fields = ('name', 'description','group','group__name')
    search_fields = ('name', 'description','group__name')
    def get_queryset(self):
        return get_all_user_objects(self.request.user, ['view'], Study)
    
class SampleViewSet(viewsets.ModelViewSet):
    serializer_class = SampleSerializer
    permission_classes = [CustomPermission]
    filter_fields = ('name', 'description','study__group__name')
    search_fields = ('name', 'description')
    model = Sample
    def get_queryset(self):
        return get_all_user_objects(self.request.user, ['view'], Sample)

class ExperimentViewSet(viewsets.ModelViewSet):
    serializer_class = ExperimentSerializer
    permission_classes = [CustomPermission]
    filter_fields = ('name', 'description','sample__study__group__name')
    search_fields = ('name', 'description')
    model = Experiment
    def get_queryset(self):
        return get_all_user_objects(self.request.user, ['view'], Experiment)

class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
#     permission_classes = [CustomPermission]
#     search_fields = ('name', 'description')
    model = File
    def get_queryset(self):
        return get_all_user_objects(self.request.user, ['view'], Experiment)
    
class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
#     permission_classes = [CustomPermission]
    filter_fields = ('content_type', 'object_id')
    model = Note
    def get_queryset(self):
        return Note.objects.all()#get_all_user_objects(self.request.user, ['view'], Experiment)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
#     permission_classes = [CustomPermission]
    filter_fields = ('permissions__codename','name') #@todo: upgrade django-rest-framework to fix this: https://github.com/tomchristie/django-rest-framework/pull/1836
    search_fields=['name']
    model = Group
    def get_queryset(self):
        return Group.objects.all().order_by('id')#get_all_user_objects(self.request.user, ['view'], Experiment)