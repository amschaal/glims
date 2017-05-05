from rest_framework import viewsets
# from models import 
from models import Log, Category, Export
from serializers import LogSerializer
from tracker.serializers import CategorySerializer, ExportSerializer

class LogViewSet(viewsets.ModelViewSet):
    serializer_class = LogSerializer
#     permission_classes = [CustomPermission]
#     search_fields = ('name', 'description')
    model = Log
#     filter_fields = ('project',)
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
    queryset = Export.objects.all()