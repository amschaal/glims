from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
# from glims.jobs import JobFactory
from glims.lims import Project, Sample, ModelType
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from permissions.manage import get_all_user_objects, has_all_permissions
# from models import 
from django.core.exceptions import ObjectDoesNotExist
from glims.serializers import *
from rest_framework import filters, generics
from django.views.generic.base import View
from django.http import JsonResponse    
from django.contrib.auth.decorators import login_required
import os
from django_compute.utils import sizeof_fmt
from glims.models import StatusOption
from django.db.models.query import Prefetch
from glims.forms import FullSampleForm


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

# @api_view(['POST'])
# # @permission_classes((ServerAuth, ))  
# def update_job(request, job_id):
#     status = request.data.get('status')
#     data = request.data.get('data',{})
#     job = JobFactory.get_job(job_id)
#     job.data.update(data)
#     job.update_status(status)
#     return Response({})

def get_cart(cart):
#     cart = request.session['sample_cart']
    
    return dict((s.id,SampleSerializer(s).data) for s in Sample.objects.filter(pk__in=cart).select_related('project__name'))
    
@api_view(['POST','GET'])
def add_samples_to_cart(request):
    sample_ids = request.data.get('sample_ids',[])
    cart = request.session.get('sample_cart', [])
#     samples = 
    cart+=Sample.objects.filter(pk__in=sample_ids).values_list('id',flat=True)
    request.session['sample_cart'] = cart   
#     for sample in samples:
#         print SampleSerializer(sample).data
#         cart[str(sample.id)] = SampleSerializer(sample).data
    return Response(get_cart(cart))

@api_view(['POST'])
def remove_samples_from_cart(request):
    sample_ids = request.data.get('sample_ids',[])
    cart = request.session.get('sample_cart', {})
    for sample_id in sample_ids:
        if sample_id in cart:
            cart.remove(sample_id)
#         cart.pop(str(sample_id),None)
    request.session['sample_cart'] = cart
    return Response(get_cart(cart))

@api_view(['POST'])
def remove_pool_samples(request,pk):
    sample_ids = request.data.get('sample_ids',[])
    pool = Pool.objects.get(pk=pk)
    for s in Sample.objects.filter(id__in=sample_ids):
        pool.samples.remove(s)
        pool.sample_data.pop(str(s.id),None)
    pool.save()
    return Response({'status':'ok'})

@api_view(['POST'])
def add_pool_samples(request,pk):
    sample_ids = request.data.get('sample_ids',[])
    pool = Pool.objects.get(pk=pk)
    for s in Sample.objects.filter(id__in=sample_ids):
        pool.samples.add(s)
    return Response({'status':'ok'})

@api_view(['POST'])
def update_pool(request,pk):
    from glims.forms import PoolForm
    pool = Pool.objects.get(pk=pk)
#     plugins = workflow.plugins.filter(page='workflow')
    form = PoolForm(request.data,instance=pool)
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
    original_data = request.data.copy()
    data = request.data.pop('data')
    pool_data.update(request.data)
    pool_data['data'].update(data)
    
#     plugins = workflow.plugins.filter(page='workflow')
    form = PoolForm(pool_data,instance=pool)
    if form.is_valid():
        pool.sample_data[str(sample_id)] = original_data
        pool.save()
        return Response({'status':'ok','data':original_data})
    else:
        return Response({'errors':form.errors})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    filter_fields = {'first_name':['exact', 'icontains'],'last_name':['icontains'],'email':['exact', 'icontains'],'groups__id':['exact'],'groups__name':['exact']} 
    search_fields=('first_name','last_name','email')
    model = User
    def get_queryset(self):
        return User.objects.all().order_by('id')
    
class ModelTypeSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ModelTypeSerializer
    permission_classes = [CustomPermission]
    filter_fields = {'content_type':['exact'],'description':['exact', 'icontains'],'name':['exact', 'icontains'],'content_type__model':['exact', 'icontains']}
    search_fields = ('content_type__model', 'name','description')
    ordering_fields = ('content_type__model', 'name')
    model = ModelType
    queryset = ModelType.objects.all()
#     def get_queryset(self):
#         return get_all_user_objects(self.request.user, ['view'], Experiment)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [CustomPermission]
    model = Project
    filter_fields = {'name':['exact', 'icontains'], 'description':['exact', 'icontains'],'lab':['exact'],'lab__name':['exact', 'icontains'],'type__name':['exact', 'icontains']}
    search_fields = ('name', 'description','lab__name','type__name')
    def get_queryset(self):
        return get_all_user_objects(self.request.user, ['view'], Project).prefetch_related(
#             Prefetch('statuses', queryset=ProjectStatus.objects.select_related('status').order_by('timestamp')),
            Prefetch('type__status_options', queryset=StatusOption.objects.select_related('status').order_by('order')))
    
class SampleViewSet(viewsets.ModelViewSet):
    serializer_class = SampleSerializer
#     permission_classes = [CustomPermission]
    filter_fields = {'sample_id':['exact', 'icontains'],'name':['exact', 'icontains'], 'project__name':['exact', 'icontains'],'project':['exact'], 'description':['exact', 'icontains'],'project__lab__name':['exact', 'icontains'],'type__name':['exact', 'icontains']}
    ordering_fields = ('sample_id','name', 'description','project__name','received','created','type__name')
    search_fields = ('name', 'description','project__name')
    model = Sample
#     def get_queryset(self):
#         return get_all_user_objects(self.request.user, ['view'], Sample)
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Sample.objects.all()
        pool = self.request.query_params.get('pool', None)
        if pool is not None:
            queryset = queryset.filter(pools__id=pool)
        return queryset
#     def create(self,request):
#         form = FullSampleForm(request.data)
#         if form.is_valid():
#             sample = form.save()
#             return Response(SampleSerializer(sample).data)
#         else:
#             return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
#     def update(self,request,pk=None):
#         instance = Sample.objects.get(id=pk)
#         form = FullSampleForm(request.data,instance=instance)
#         if form.is_valid():
#             sample = form.save()
#             return Response(SampleSerializer(sample).data)
#         else:
#             return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class PoolViewSet(viewsets.ModelViewSet):
    serializer_class = PoolSerializer
    permission_classes = [CustomPermission]
    filter_fields = {'name':['exact', 'icontains'], 'description':['exact', 'icontains'],'type__name':['exact', 'icontains']}
    ordering_fields = ('name', 'created','type__name')
    search_fields = ('name', 'description','type__name')
    model = Pool
    def get_queryset(self):
        return get_all_user_objects(self.request.user, ['view'], Pool)
    
# class JobSubmissionViewset(viewsets.ReadOnlyModelViewSet):
#     model = JobSubmission
#     serializer_class = JobSubmissionSerializer
#     search_fields = ('name', 'description','type','status','id')
#     ordering_fields = ('name')
# #     filter_fields = ('type','status')
    
class JobViewset(viewsets.ReadOnlyModelViewSet):
    model = Job
    serializer_class = JobSerializer
    search_fields = ('id', 'job_id','script_path','status')
    ordering_fields = ('created','run','status','id')
    ordering = ('-created')
    filter_fields = {'template__id':['exact', 'icontains'],'status':['exact', 'icontains'],'id':['exact', 'icontains']}
    def get_queryset(self):
        return Job.objects.all().order_by('-created')
    
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

class LabViewSet(viewsets.ModelViewSet):
    serializer_class = LabSerializer
#     permission_classes = [CustomPermission]
    filter_fields = {'name':['exact', 'icontains'],'description':['icontains']} #@todo: upgrade django-rest-framework to fix this: https://github.com/tomchristie/django-rest-framework/pull/1836
    search_fields=('name','description')
    model = Lab
    def get_queryset(self):
        return Lab.objects.all().order_by('id')#get_all_user_objects(self.request.user, ['view'], Experiment)

# class TemplateResponseMixin(object):
#     """
#     A mixin that can be used to render a template.
#     """
#     template_name = None
#     response_class = TemplateResponse
#     content_type = None
# 
#     def render_to_response(self, context, **response_kwargs):
#         """
#         Returns a response, using the `response_class` for this
#         view, with a template rendered with the given context.
# 
#         If any keyword arguments are provided, they will be
#         passed to the constructor of the response class.
#         """
#         response_kwargs.setdefault('content_type', self.content_type)
#         return self.response_class(
#             request=self.request,
#             template=self.get_template_names(),
#             context=context,
#             **response_kwargs
#         )
# 
#     def get_template_names(self):
#         """
#         Returns a list of template names to be used for the request. Must return
#         a list. May not be called if render_to_response is overridden.
#         """
#         if self.template_name is None:
#             raise ImproperlyConfigured(
#                 "TemplateResponseMixin requires either a definition of "
#                 "'template_name' or an implementation of 'get_template_names()'")
#         else:
#             return [self.template_name]

class FormMixin(object):
    form_class = None
    lookup_field = 'pk'
    kwarg_field = 'pk'
    model = None
    def get_form_class(self,request,*args,**kwargs):
        return self.form_class
    def get_instance(self,request,*args,**kwargs):
        if not self.model:
            return None
        return self.model.objects.get(**{self.lookup_field:kwargs[self.kwarg_field]})
    

class FormView(FormMixin,View):
    """
    A view that renders a template.  This view will also pass into the context
    any keyword arguments passed by the url conf.
    """
    def post(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context)
        import json
        form_class = self.get_form_class(request,*args,**kwargs)
        instance = self.get_instance(request,*args,**kwargs)
        if instance:
            form = form_class(json.loads(request.body),instance=instance)
        else:
            form = form_class(json.loads(request.body))
        if form.is_valid():
            form.save()
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'errors':form.errors})

# class AjaxFormView(object):
#     def __init__(self):
#         pass
#     def get_form_class(self,request,**kwargs):
#         pass
#     def get_instance(self,request,**kwargs):
#         return None
#     def view(self,request,**kwargs):
#         import json
#         form_class = self.get_form(request,**kwargs)
#         instance = self.get_instance(request,**kwargs)
#         if request.method == 'POST':
#             if instance:
#                 form = form_class(json.loads(request.body),instance=instance)
#             else:
#                 form = form_class(json.loads(request.body))
#             if form.is_valid():
#                 return Response({'status':'ok'})
#             else:
#                 return Response({'errors':form.errors}) 
# class ProcessFormView(AjaxFormView):
#     def get_form_class(self, request, **kwargs):
#         from glims.forms import ProcessForm
#         return ProcessForm
#     def get_instance(self, request, **kwargs):
#         from glims.lims import Process
#         return Process.objects.get(pk=kwargs['pk'])
#         
#     
# from django.views.generic import TemplateView        

@login_required
def project_files(request,project_id,path):
    path = path if path else ''
    project = Project.objects.get(id=project_id)
    if not project.directory:
        raise Exception("This project does not have a directory specified.")
    if path.count('..') != 0:
        raise Exception("Path may not contain '..'")
    if path.startswith('/'):
        raise Exception("Path may not start with '/'")
    full_path = os.path.join(project.directory,path)
    filenames=[]
    directories=[]
    for (dirpath, dirnames, filenames) in os.walk(full_path):
        fileinfo = [{'name':file,'stats':os.stat(os.path.join(full_path,file))} for file in filenames]
        directories=dirnames
        break
#     {'name':file['name'],'size':sizeof_fmt(file['stats'].st_size),'bytes':file['stats'].st_size,'modified':datetime.datetime.fromtimestamp(file['stats'].st_mtime).strftime("%m/%d/%Y %I:%M %p")
    files = [{'name':file['name'], 'size':sizeof_fmt(file['stats'].st_size)} for file in fileinfo]
    return JsonResponse({'project_id':project_id,'path':path,'files':files,'directories':directories})
        