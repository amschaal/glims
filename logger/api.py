from rest_framework import viewsets
# from models import 
from logger.models import Log
from logger.serializers import LogSerializer

class LogViewSet(viewsets.ModelViewSet):
    serializer_class = LogSerializer
#     permission_classes = [CustomPermission]
    model = Log
    filter_fields = {'content_type':['exact'], 'object_id':['exact'],'text':['icontains'],'description':['icontains']}
    queryset = Log.objects.all()
