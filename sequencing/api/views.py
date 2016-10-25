from rest_framework import viewsets
from sequencing.api.serializers import RunSerializer, MachineSerializer
from sequencing.models import Run, Machine

class RunViewSet(viewsets.ModelViewSet):
    serializer_class = RunSerializer
    model = Run
    filter_fields = {'machine__name':['icontains'],'description':['icontains']}#,'lanes__pool__library__name':['icontains'],'lanes__pool__name':['icontains']
    queryset = Run.objects.all()

class MachineViewSet(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    model = Machine
#     filter_fields = {'machine__name':['icontains'],'description':['icontains']}#,'lanes__pool__library__name':['icontains'],'lanes__pool__name':['icontains']
    queryset = Machine.objects.all()