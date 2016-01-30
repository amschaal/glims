from django.contrib.auth.models import User
from django.db.models.query import Prefetch
from rest_framework import viewsets

from django_compute.models import Job
from extensible.models import ModelType
# from glims.api.permissions import CustomPermission
from glims.api.serializers import UserSerializer, ModelTypeSerializer, \
    ProjectSerializer, SampleSerializer, PoolSerializer, JobSerializer, \
    LabSerializer
from glims.lims import Project, Sample, Pool, Lab
from glims.models import StatusOption
from glims.api.filters import HstoreFilter, HstoreOrderFilter
# from glims.permissions.manage import get_all_user_objects


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    filter_fields = {'first_name':['exact', 'icontains'],'last_name':['icontains'],'email':['exact', 'icontains'],'groups__id':['exact'],'groups__name':['exact']} 
    search_fields=('first_name','last_name','email')
    model = User
    def get_queryset(self):
        return User.objects.all().order_by('id')

class ExtensibleViewset(viewsets.ModelViewSet):
    hstore_field = 'data'
    def __init__(self,*args,**kwargs):
        super(ExtensibleViewset, self).__init__(*args,**kwargs)
        self.filter_backends += (HstoreFilter,HstoreOrderFilter)
#     def get_queryset(self):
#         print 'GET queryset'
#         qs = super(ExtensibleViewset, self).get_queryset()
#         filters = {}
#         for key,value in self.request.query_params.items():
#             if key.starts_with('data__'):
#                 filters[key]=value
#         print 'FILTERS!!!!'
#         print filters
#         return qs.filter(**filters)
#     filter_backends = (HstoreFilter,)
    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        print self.request.method
        print args
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if self.request.method in ['POST','PUT','PATCH']:
            kwargs['fields'] = self.get_model_type_fields(*args, **kwargs)
#             print kwargs['data']['type']['id']
        return serializer_class(*args, **kwargs)
    def get_model_type_fields(self,*args,**kwargs):
        try: #If a type object with "id" is sent
            type_id = kwargs['data']['type']['id']
        except:
            try: #If a type is sent as an integer
                type_id = int(kwargs['data']['type'])
            except:
                type_id = None
        if type_id: #return fields for sent type id
            return ModelType.objects.get(id=type_id).fields
        try: #Otherwise, if the object already has a type, use its fields
            if type(args[0].type) == ModelType:
                return args[0].type.fields
            return []
        except:
            return []

class ModelTypeSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ModelTypeSerializer
#     permission_classes = [CustomPermission]
    filter_fields = {'content_type':['exact'],'description':['exact', 'icontains'],'name':['exact', 'icontains'],'content_type__model':['exact', 'icontains']}
    search_fields = ('content_type__model', 'name','description')
    ordering_fields = ('content_type__model', 'name')
    model = ModelType
    queryset = ModelType.objects.all()
#     def get_queryset(self):
#         return get_all_user_objects(self.request.user, ['view'], Experiment)

class ProjectViewSet(ExtensibleViewset):
    serializer_class = ProjectSerializer
#     permission_classes = [CustomPermission]
    model = Project
    filter_fields = {'name':['exact', 'icontains'], 'description':['exact', 'icontains'],'lab':['exact'],'lab__name':['exact', 'icontains'],'type__name':['exact', 'icontains']}
    search_fields = ('name', 'description','lab__name','type__name')
    def get_queryset(self):
#         return get_all_user_objects(self.request.user, ['view'], Project).prefetch_related(
          return Project.objects.prefetch_related(  
#             Prefetch('statuses', queryset=ProjectStatus.objects.select_related('status').order_by('timestamp')),
            Prefetch('type__status_options', queryset=StatusOption.objects.select_related('status').order_by('order')))
    

class SampleViewSet(ExtensibleViewset):
    serializer_class = SampleSerializer
#     permission_classes = [CustomPermission]
    filter_fields = {'sample_id':['exact', 'icontains'],'name':['exact', 'icontains'], 'project__name':['exact', 'icontains'],'project':['exact'], 'description':['exact', 'icontains'],'project__lab__name':['exact', 'icontains'],'type__name':['exact', 'icontains'],'data':['contains']}
    ordering_fields = ('id','sample_id','name', 'description','project__name','received','created','type__name')
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
    
class PoolViewSet(ExtensibleViewset):
    serializer_class = PoolSerializer
#     permission_classes = [CustomPermission]
    filter_fields = {'name':['exact', 'icontains'], 'description':['exact', 'icontains'],'type__name':['exact', 'icontains']}
    ordering_fields = ('name', 'created','type__name')
    search_fields = ('name', 'description','type__name')
    model = Pool
    def get_queryset(self):
        return Pool.objects.all()
#         return get_all_user_objects(self.request.user, ['view'], Pool)
        

class JobViewset(viewsets.ReadOnlyModelViewSet):
    model = Job
    serializer_class = JobSerializer
    search_fields = ('id', 'job_id','script_path','status')
    ordering_fields = ('created','run','status','id')
    ordering = ('-created')
    filter_fields = {'template__id':['exact', 'icontains'],'status':['exact', 'icontains'],'id':['exact', 'icontains']}
    def get_queryset(self):
        return Job.objects.all().order_by('-created')

class LabViewSet(viewsets.ModelViewSet):
    serializer_class = LabSerializer
#     permission_classes = [CustomPermission]
    filter_fields = {'name':['exact', 'icontains'],'description':['icontains']} #@todo: upgrade django-rest-framework to fix this: https://github.com/tomchristie/django-rest-framework/pull/1836
    search_fields=('name','description')
    model = Lab
    def get_queryset(self):
        return Lab.objects.all().order_by('id')#get_all_user_objects(self.request.user, ['view'], Experiment)