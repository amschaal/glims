from proteomics.models import FastaFile, ParameterFile
from rest_framework import viewsets
from proteomics.api.serializers import FastaFileSerializer, ParameterFileSerializer

class FastaFileViewSet(viewsets.ModelViewSet):
    serializer_class = FastaFileSerializer
    model = FastaFile
    filter_fields = {'name':['exact','icontains'], 'description':['exact','icontains']}
    search_fields = ('name', 'description')
    queryset = FastaFile.objects.all()

class ParameterFileViewSet(viewsets.ModelViewSet):
    serializer_class = ParameterFileSerializer
    model = ParameterFile
    queryset = ParameterFile.objects.all()
    search_fields = ('name', 'description')