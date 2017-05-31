from rest_framework import viewsets, filters
# from models import 
from models import Log, Category, Export
from serializers import LogSerializer
from tracker.serializers import CategorySerializer, ExportSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.settings import api_settings
from tracker.csvrenderer import PaginatedCSVRenderer


class ExcludeExportFilter(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        export_id = view.request.query_params.get('exclude_export',None)
        if not export_id:
            return queryset
        return queryset.exclude(exports__id__in=[export_id])

class LogViewSet(viewsets.ModelViewSet):
    serializer_class = LogSerializer
    filter_backends = viewsets.ModelViewSet.filter_backends + [ExcludeExportFilter]
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES+[PaginatedCSVRenderer]
#     permission_classes = [CustomPermission]
#     search_fields = ('name', 'description')
    model = Log
    filter_fields = {'exports__id':['exact'],'project':['exact'],'status':['exact','icontains'],'user__last_name':['icontains'],'category__name':['icontains'],'project__name':['icontains'],'description':['icontains'],'project__lab__last_name':['icontains']}
    multi_field_filters = {'user_name':['user__last_name__icontains','user__first_name__icontains'],'lab_name':['project__lab__first_name__icontains','project__lab__last_name__icontains']}
    ordering_fields = ('modified', 'status','user__last_name','quantity','category__name','project__name','project__lab__last_name')
    queryset = Log.objects.select_related('user','category').all()
    @list_route(methods=['post'])
    def set_statuses(self,request):
        status = request.data.get('status')
        log_ids = request.data.get('log_ids',[])
        Log.objects.filter(id__in=log_ids).update(status=status)
        return Response({'status':'ok'})
    
#     def get_queryset(self):
#         return File.objects.all()
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    model = Category
    queryset = Category.objects.all()

class ExportViewSet(viewsets.ModelViewSet):
    serializer_class = ExportSerializer
    model = Export
    queryset = Export.objects.all()
    #Changes to logs are not being shown on update.  Trying a hacky method around it...
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         instance = self.get_object() #get object over again from updated database
#         serializer = self.get_serializer(instance) #serialize object
#         return Response(serializer.data)
    @detail_route(methods=['post'])
    def remove_logs(self,request,pk):
        export = self.get_object()
        log_ids = request.data.get('log_ids',[])
        for l in Log.objects.filter(id__in=log_ids):
            export.logs.remove(l)
        return Response({'status':'ok'})
    @detail_route(methods=['post'])
    def add_logs(self,request,pk):
        export = self.get_object()
        log_ids = request.data.get('log_ids',[])
        for l in Log.objects.filter(id__in=log_ids):
            export.logs.add(l)
        return Response({'status':'ok'})
