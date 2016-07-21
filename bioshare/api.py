from rest_framework import viewsets
# from models import 
from bioshare.serializers import ProjectShareSerializer
from bioshare.models import ProjectShare

class ProjectShareViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectShareSerializer
    model = ProjectShare
    filter_fields = ('project',)
    queryset = ProjectShare.objects.all()
