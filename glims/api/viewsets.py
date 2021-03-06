from django.contrib.auth.models import User, Group
from django.db.models.query import Prefetch
from rest_framework import viewsets, status

from django_compute.models import Job
from extensible.drf.viewsets import ExtensibleViewset
from extensible.models import ModelType
from glims.api.serializers import UserSerializer, ModelTypeSerializer, \
    ProjectSerializer, SampleSerializer, PoolSerializer, JobSerializer, \
    LabSerializer, GroupSerializer, StatusSerializer, UserProfileSerializer,\
    LibrarySerializer, AdapterSerializer, ProjectNoteSerializer
from glims.models import Project, Sample, Pool, Lab, UserProfile, \
    Library, Adapter
from glims.api.permissions import GroupPermission, AdminOrReadOnlyPermission
from rest_framework.permissions import IsAuthenticated
from glims.models import Status
from rest_framework.decorators import detail_route, list_route
from glims.api.mixins import FileManagerMixin 
from django.db.models.query_utils import Q
from glims.api.filters import FollowingProjectFilter, ProjectStatusFilter,\
    ParticipantFilter, ProjectAttachmentFilter, AttachmentTags, HasIssuesFilter
from rest_framework.response import Response
from glims.samples.importer import ProjectExport
from rest_framework.exceptions import PermissionDenied
from attachments.api import NoteViewSet
from attachments.models import Note


# from glims.api.permissions import CustomPermission
# from glims.permissions.manage import get_all_user_objects
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    filter_fields = {'first_name':['exact', 'icontains'],'last_name':['icontains'],'email':['exact', 'icontains'],'groups__id':['exact'],'groups__name':['exact'],'id':['gte','exact']} 
    search_fields=('first_name','last_name','email')
    model = User
    def get_queryset(self):
        return User.objects.all().order_by('id')
    @list_route(methods=['get','post'],permission_classes=[IsAuthenticated])
    def profile(self, request, pk=None):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if request.method == 'GET':
            serializer = UserProfileSerializer(profile)
        if request.method == 'POST':
            serializer = UserProfileSerializer(profile,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
#     @list_route(methods=['post'],permission_classes=[IsAuthenticated])
#     def profile(self, request, pk=None):
#         serializer = UserProfileSerializer(request.user,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupSerializer
    model = Group
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Group.objects.all().order_by('id')
        return self.request.user.groups.all()

class ModelTypeSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = ModelTypeSerializer
    permission_classes = [IsAuthenticated,AdminOrReadOnlyPermission]
    filter_fields = {'content_type':['exact'],'description':['exact', 'icontains'],'name':['exact', 'icontains'],'content_type__model':['exact', 'icontains']}
    search_fields = ('content_type__model', 'name','description')
    ordering_fields = ('content_type__model', 'name')
    model = ModelType
    queryset = ModelType.objects.all()
#     def get_queryset(self):
#         return get_all_user_objects(self.request.user, ['view'], Experiment)

class StatusSerializerViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated,AdminOrReadOnlyPermission]
    filter_fields = {'model_type':['exact']}
#     ordering_fields = ('content_type__model', 'name')
    model = Status
    queryset = Status.objects.all()

class ProjectViewSet(ExtensibleViewset,FileManagerMixin):
    serializer_class = ProjectSerializer
#     permission_classes = [CustomPermission]
    filter_backends = ExtensibleViewset.filter_backends + [FollowingProjectFilter,ProjectStatusFilter,ParticipantFilter,HasIssuesFilter]
    permission_classes = [IsAuthenticated,GroupPermission]
    model = Project
    filter_fields = {'project_id':['exact','icontains'],'name':['exact', 'icontains'], 'description':['icontains'],'contact':['icontains'],'lab':['exact'],'type':['exact'],'type__name':['exact', 'icontains'],'group__id':['exact','in'],'group__name':['icontains','exact'],'archived':['exact'],'manager__last_name':['icontains'],'participants__last_name':['icontains'],'status__name':['icontains'],'created':['gte','lte','lt','gt']}
    search_fields = ('name', 'description','type__name','lab__first_name','lab__last_name','project_id')
    multi_field_filters = {'manager':['manager__last_name__icontains','manager__first_name__icontains'],'participants':['participants__last_name__icontains','participants__first_name__icontains'],'lab_name':['lab__first_name__icontains','lab__last_name__icontains']}
    ordering_fields = ('created','modified', 'id','project_id','name','type','type__name','description','manager__last_name','status__name','lab__last_name','group__name','archived')
    def get_queryset(self):
        return Project.objects.select_related('type','sample_type','manager','lab','group').prefetch_related(  
#             Prefetch('statuses', queryset=ProjectStatus.objects.select_related('status').order_by('timestamp')),
            Prefetch('type__status_options'),Prefetch('participants'),Prefetch('related_projects'))#, queryset=Status.objects.order_by('order')
    @list_route(methods=['get'],permission_classes=[IsAuthenticated])
    def export(self, request):
        queryset = self.filter_queryset(self.get_queryset())#self.get_queryset()
        type = request.query_params.get('type')
        format = request.query_params.get('file_format','xls')
#         queryset = queryset.filter(type=type)
        exporter = ProjectExport(type=type)
        return exporter.export(request,queryset,file_type=format)

class SampleViewSet(ExtensibleViewset,FileManagerMixin):
    serializer_class = SampleSerializer
#     permission_classes = [CustomPermission]
    permission_classes = [IsAuthenticated,GroupPermission]
    filter_fields = {'sample_id':['exact', 'icontains'],'name':['exact', 'icontains'], 'project__name':['exact', 'icontains'],'project':['exact'], 'description':['exact', 'icontains'],'type__name':['exact', 'icontains'],'project__lab':['exact']}
    multi_field_filters = {'lab_name':['project__lab__first_name__icontains','project__lab__last_name__icontains']}
    ordering_fields = ('id','sample_id','name', 'description','project__name','received','created','type__name')
    search_fields = ('name', 'description','project__name')
    model = Sample
#     def get_queryset(self):
#         return get_all_user_objects(self.request.user, ['view'], Sample)
    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

#         Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
# 
#         assert lookup_url_kwarg in self.kwargs, (
#             'Expected view %s to be called with a URL keyword argument '
#             'named "%s". Fix your URL conf, or set the `.lookup_field` '
#             'attribute on the view correctly.' %
#             (self.__class__.__name__, lookup_url_kwarg)
#         )
# 
#         filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        
#         obj = get_object_or_404(queryset, **filter_kwargs)
        try:
            obj = queryset.get(sample_id=self.kwargs[lookup_url_kwarg])
        except:
            obj = queryset.get(id=self.kwargs[lookup_url_kwarg])
#         obj = queryset.get(Q(sample_id=self.kwargs[lookup_url_kwarg])|Q(id=self.kwargs[lookup_url_kwarg]))

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj
    def get_queryset(self):
        queryset = Sample.objects.select_related('type','project').all()
        pool = self.request.query_params.get('pool', None)
        if pool is not None:
            queryset = queryset.filter(pools__id=pool)
        return queryset
    
class PoolViewSet(ExtensibleViewset):
    serializer_class = PoolSerializer
#     permission_classes = [CustomPermission]
    permission_classes = [IsAuthenticated,GroupPermission]
    filter_fields = {'name':['exact', 'icontains'], 'description':['exact', 'icontains'],'type__name':['exact', 'icontains'],'project':['exact','in']}
    ordering_fields = ('name', 'created','type__name')
    search_fields = ('name', 'description','type__name')
    model = Pool
    def get_queryset(self):
        return Pool.objects.select_related('group','type').prefetch_related('libraries','libraries__adapter','libraries__sample','libraries__sample__project__lab').all()
#         return get_all_user_objects(self.request.user, ['view'], Pool)

class AdapterViewSet(ExtensibleViewset):
    serializer_class = AdapterSerializer
    permission_classes = [IsAuthenticated]#,GroupPermission
#     filter_fields = {'name':['exact', 'icontains'], 'description':['exact', 'icontains'],'type__name':['exact', 'icontains']}
#     ordering_fields = ('name', 'created','type__name')
#     search_fields = ('name', 'description','type__name')
    model = Adapter
    def get_queryset(self):
        return Adapter.objects.all()

class LibraryViewSet(ExtensibleViewset):
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated,GroupPermission]
    filter_fields = {'sample':['exact'],'sample__sample_id':['exact', 'icontains'],'sample__name':['exact', 'icontains'], 'sample__project__name':['exact', 'icontains'],'sample__project':['exact'], 'description':['exact', 'icontains'],'sample__type__name':['exact', 'icontains'],'sample__project__lab':['exact']}
#     multi_field_filters = {'lab_name':['project__lab__first_name__icontains','project__lab__last_name__icontains']}
    ordering_fields = ('id','sample__sample_id','name', 'description','sample__project__name','sample__received','created','type__name','adapter__name')
    model = Library
    def get_queryset(self):
        queryset = Library.objects.select_related('sample','adapter','type').prefetch_related('pools').all()
        pool = self.request.query_params.get('pool', None)
        if pool is not None:
            queryset = queryset.filter(pools__id=pool)
        return queryset

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
    filter_fields = {'description':['icontains']} #@todo: upgrade django-rest-framework to fix this: https://github.com/tomchristie/django-rest-framework/pull/1836
    multi_field_filters = {'name':['first_name__icontains','last_name__icontains'],'affiliation':['affiliation__exact', 'affiliation__icontains']}
    search_fields=('first_name','last_name','description')
    model = Lab
    def get_queryset(self):
        return Lab.objects.all().order_by('id')#get_all_user_objects(self.request.user, ['view'], Experiment)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.projects.all().count() > 0:
            raise PermissionDenied('Labs with projects may not be deleted.  Delete or reassign all lab projects before attempting to delete this lab.')
        return super(LabViewSet, self).destroy(request,*args,**kwargs)

class ExtendedNoteViewSet(NoteViewSet):
    filter_backends = ExtensibleViewset.filter_backends + [ProjectAttachmentFilter,AttachmentTags]#]
    serializer_class = ProjectNoteSerializer
    queryset = Note.objects.all().prefetch_related('content_object')