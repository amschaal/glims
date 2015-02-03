from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONPRenderer, JSONRenderer
from glims.jobs import JobFactory
from glims.lims import Project, Sample, ModelType
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from permissions.manage import get_all_user_objects, has_all_permissions
# from models import 
from django.core.exceptions import ObjectDoesNotExist
from glims.serializers import *
from rest_framework import filters, generics


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
    data = request.DATA.get('data',{})
    job = JobFactory.get_job(job_id)
    job.data.update(data)
    job.update_status(status)
    return Response({})

@api_view(['POST'])
def add_samples_to_cart(request):
    sample_ids = request.DATA.get('sample_ids',[])
    cart = request.session.get('sample_cart', {})
    samples = Sample.objects.filter(pk__in=sample_ids)
    for sample in samples:
        cart[str(sample.id)] = SampleSerializer(sample).data
    request.session['sample_cart'] = cart
    return Response(cart)

@api_view(['POST'])
def remove_samples_from_cart(request):
    sample_ids = request.DATA.get('sample_ids',[])
    cart = request.session.get('sample_cart', {})
    for sample_id in sample_ids:
        cart.pop(str(sample_id),None)
    request.session['sample_cart'] = cart
    return Response(cart)

@api_view(['POST'])
def remove_pool_samples(request,pk):
    sample_ids = request.DATA.get('sample_ids',[])
    pool = Pool.objects.get(pk=pk)
    for s in Sample.objects.filter(id__in=sample_ids):
        pool.samples.remove(s)
        pool.sample_data.pop(str(s.id),None)
    pool.save()
    return Response({'status':'ok'})

@api_view(['POST'])
def add_pool_samples(request,pk):
    sample_ids = request.DATA.get('sample_ids',[])
    pool = Pool.objects.get(pk=pk)
    for s in Sample.objects.filter(id__in=sample_ids):
        pool.samples.add(s)
    return Response({'status':'ok'})

@api_view(['POST'])
def update_pool(request,pk):
    from glims.forms import PoolForm
    pool = Pool.objects.get(pk=pk)
#     plugins = workflow.plugins.filter(page='workflow')
    form = PoolForm(request.DATA,instance=pool)
    if form.is_valid():
        form.save()
        return Response({'status':'ok','data':PoolSerializer(pool).data})
    else:
        return Response({'errors':form.errors})
@api_view(['POST'])
def update_pool_sample(request,pool_id,sample_id):
    from glims.forms import PoolForm
    pool = Pool.objects.get(pk=pool_id)
    pool_data = PoolSerializer(pool).data
    original_data = request.DATA.copy()
    data = request.DATA.pop('data')
    pool_data.update(request.DATA)
    pool_data['data'].update(data)
    
#     plugins = workflow.plugins.filter(page='workflow')
    form = PoolForm(pool_data,instance=pool)
    if form.is_valid():
        pool.sample_data[str(sample_id)] = original_data
        pool.save()
        return Response({'status':'ok','data':original_data})
    else:
        return Response({'errors':form.errors})
    
    
@api_view(['POST'])
def update_workflow(request,pk):
    from glims.forms import WorkflowForm
    workflow = Workflow.objects.get(pk=pk)
#     plugins = workflow.plugins.filter(page='workflow')
    form = WorkflowForm(request.DATA,instance=workflow)
    if form.is_valid():
        form.save()
        return Response({'status':'ok','data':WorkflowSerializer(workflow).data})
    else:
        return Response({'errors':form.errors})    
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
#     permission_classes = [CustomPermission]
    filter_fields = ('name', 'project', 'description','project__group__name')
    ordering_fields = ('name', 'project__name','received')
    search_fields = ('name', 'description')
    model = Sample
#     def get_queryset(self):
#         return get_all_user_objects(self.request.user, ['view'], Sample)
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Sample.objects.all()
        pool = self.request.QUERY_PARAMS.get('pool', None)
        if pool is not None:
            queryset = queryset.filter(pools__id=pool)
        return queryset
    
class PoolViewSet(viewsets.ModelViewSet):
    serializer_class = PoolSerializer
    permission_classes = [CustomPermission]
    filter_fields = ('name','type__name')
    ordering_fields = ('name', 'created','type__name')
    search_fields = ('name', 'description','type__name')
    model = Pool
    def get_queryset(self):
        return get_all_user_objects(self.request.user, ['view'], Pool)
    
class WorkflowViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowSerializer
    filter_fields = ('name','type__name')
    ordering_fields = ('name', 'created','type__name')
    search_fields = ('name', 'description','type__name')
    model = Workflow

class JobSubmissionViewset(viewsets.ReadOnlyModelViewSet):
    model = JobSubmission
    serializer_class = JobSubmissionSerializer
    search_fields = ('name', 'description','type','status','id')
    ordering_fields = ('name')
#     filter_fields = ('type','status')
    
class JobViewset(viewsets.ReadOnlyModelViewSet):
    model = Job
    serializer_class = JobSerializer
    search_fields = ('name', 'description','type','status','job_id')
    ordering_fields = ('name','type','status','job_id')
    filter_fields = ('type','status')
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