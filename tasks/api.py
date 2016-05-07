from rest_framework import viewsets
from models import Task
from serializers import *

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
#     permission_classes = [CustomPermission]
    filter_fields = ('project',)
    model = Task
    queryset = Task.objects.all()
#     def get_queryset(self):
#         return Note.objects.all()#get_all_user_objects(self.request.user, ['view'], Experiment)
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)