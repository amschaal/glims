from rest_framework import viewsets
from sequencing.api.serializers import RunSerializer
from sequencing.models import Run

class RunViewSet(viewsets.ModelViewSet):
    serializer_class = RunSerializer
    model = Run
    filter_fields = {'machine__name':['icontains'],'description':['icontains']}#,'lanes__pool__library__name':['icontains'],'lanes__pool__name':['icontains']
    queryset = Run.objects.all()
