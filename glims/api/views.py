import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse    
from django.views.generic.base import View
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django_compute.utils import sizeof_fmt
from glims.api.serializers import SampleSerializer, PoolSerializer
from glims.lims import Sample, Pool, Project
from django.views.generic.list import ListView
from rest_framework.views import APIView


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


    
# class JobSubmissionViewset(viewsets.ReadOnlyModelViewSet):
#     model = JobSubmission
#     serializer_class = JobSubmissionSerializer
#     search_fields = ('name', 'description','type','status','id')
#     ordering_fields = ('name')
# #     filter_fields = ('type','status')
    

    
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

class FileBrowser(APIView):
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAdminUser,)
    extension_filters = []
    base_directory = None
    def get(self, request, format=None):
        if not self.base_directory:
            raise Exception("'base_directory' attribute must be set for FileBrowser view")
        dir = request.query_params.get('dir','')
        print dir
        if any(illegal in dir for illegal in ['~','..']):
            raise Exception("Illegal directory given")
        path = os.path.join(self.base_directory,dir)
        list = []
        for name in os.listdir(path):
            full_path = os.path.join(path,name)
            if os.path.isdir(full_path):
                list.append({'name':name,'is_dir':True})
            else:
                extension = os.path.splitext(full_path)[1]
                print extension
                if len(self.extension_filters) > 0:
                    if extension in self.extension_filters:
                        list.append({'name':name,'is_dir':False,'extension':extension})
                else:
                    list.append({'name':name,'is_dir':False,'extension':extension})
        return Response(list)
        