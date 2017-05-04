from rest_framework import viewsets
# from models import 
from models import Log, Category
from serializers import LogSerializer
from tracker.serializers import CategorySerializer

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