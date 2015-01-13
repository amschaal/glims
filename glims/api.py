from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONPRenderer, JSONRenderer
from glims.models import JobFactory
from glims.lims import Project, Sample, ModelType
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

@api_view(['POST'])
def add_samples_to_cart(request):
    sample_ids = request.DATA.get('sample_ids',[])
    cart = request.session.get('sample_cart', {})
    samples = Sample.objects.filter(pk__in=sample_ids)
    for sample in samples:
        cart[sample.id] = SampleSerializer(sample).data
    request.session['sample_cart'] = cart
    return Response(cart)

@api_view(['POST'])
def remove_samples_from_cart(request):
    sample_ids = request.DATA.get('sample_ids',[])
    cart = request.session.get('sample_cart', {})
    for sample_id in sample_ids:
        print sample_id
        cart.pop(str(sample_id),None)
    request.session['sample_cart'] = cart
    return Response(cart)


# class ProjectViewset(viewsets.ViewSet):
#     queryset = Project.objects.all()
#     """
#     A simple ViewSet that for listing or retrieving projects.
#     """
#     def list(self, request):
#         queryset = get_all_user_objects(request.user, ['view'], Project)
#         serializer = ProjectSerializer(queryset, many=True)
#         return Response(serializer.data)
#     def retrieve(self, request, pk=None):
#         queryset = get_all_user_objects(request.user, ['view'], Project)
#         project = get_object_or_404(queryset, pk=pk)
#         serializer = ProjectSerializer(project)
#         return Response(serializer.data)
class ModelTypeSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ModelTypeSerializer
    permission_classes = [CustomPermission]
    filter_fields = ('content_type',)
    search_fields = ('content_type', 'name','description')
    model = ModelType
#     def get_queryset(self):
#         return get_all_user_objects(self.request.user, ['view'], Experiment)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [CustomPermission]
    model = Project
    filter_fields = ('name', 'description','group','group__name')
    search_fields = ('name', 'description','group__name','type__name')
    def get_queryset(self):
        return get_all_user_objects(self.request.user, ['view'], Project)
    
class SampleViewSet(viewsets.ModelViewSet):
    serializer_class = SampleSerializer
    permission_classes = [CustomPermission]
    filter_fields = ('name', 'project', 'description','project__group__name')
    ordering_fields = ('name', 'project__name','received')
    search_fields = ('name', 'description')
    model = Sample
    def get_queryset(self):
        return get_all_user_objects(self.request.user, ['view'], Sample)
    
class PoolViewSet(viewsets.ModelViewSet):
    serializer_class = PoolSerializer
    permission_classes = [CustomPermission]
    filter_fields = ('name','type__name')
    ordering_fields = ('name', 'created','type__name')
    search_fields = ('name', 'description','type__name')
    model = Pool
    def get_queryset(self):
        return get_all_user_objects(self.request.user, ['view'], Pool)

"""
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
"""

class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
#     permission_classes = [CustomPermission]
    filter_fields = ('permissions__codename','name') #@todo: upgrade django-rest-framework to fix this: https://github.com/tomchristie/django-rest-framework/pull/1836
    search_fields=['name']
    model = Group
    def get_queryset(self):
        return Group.objects.all().order_by('id')#get_all_user_objects(self.request.user, ['view'], Experiment)