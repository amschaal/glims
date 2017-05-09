from rest_framework import viewsets
# from models import 
from models import Log, Category, Export
from serializers import LogSerializer
from tracker.serializers import CategorySerializer, ExportSerializer
from rest_framework.response import Response

class LogViewSet(viewsets.ModelViewSet):
    serializer_class = LogSerializer
#     permission_classes = [CustomPermission]
#     search_fields = ('name', 'description')
    model = Log
    filter_fields = {'project':['exact'],'status':['exact','icontains'],'user__last_name':['icontains'],'category__name':['icontains'],'project__name':['icontains'],'description':['icontains'],'project__lab__last_name':['icontains']}
    ordering_fields = ('modified', 'status','user__last_name','quantity','category__name','project__name','project__lab__last_name')
    queryset = Log.objects.all()
    
#     def get_queryset(self):
#         return File.objects.all()
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    model = Category
    queryset = Category.objects.all()

class ExportViewSet(viewsets.ModelViewSet):
    serializer_class = ExportSerializer
    model = Export
    queryset = Export.objects.prefetch_related('logs').all()
    #Changes to logs are not being shown on update.  Trying a hacky method around it...
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance = self.get_object() #get object over again from updated database
        serializer = self.get_serializer(instance) #serialize object
        return Response(serializer.data)