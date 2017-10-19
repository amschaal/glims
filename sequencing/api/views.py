from rest_framework import viewsets
from sequencing.api.serializers import RunSerializer,RunDetailSerializer, MachineSerializer
from sequencing.models import Run, Machine


#@todo: fix this... it isn't being called when used as a mixin
class ActionSerializerMixin(object):
    """
    Provide the following in model for different serializers
    action_serializers = {
        'retrieve': MyModelDetailSerializer,
        'list': MyModelListSerializer,
        'create': MyModelCreateSerializer
    }
    """
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers.keys():
                return self.action_serializers[self.action]
        return viewsets.ModelViewSet.get_serializer_class(self)


class RunViewSet(viewsets.ModelViewSet):
    action_serializers = {
        'retrieve': RunDetailSerializer,
        'list': RunSerializer,
        'create': RunDetailSerializer,
        'update': RunDetailSerializer
    }
    serializer_class = RunSerializer
    model = Run
    filter_fields = {'name':['icontains'],'machine__name':['icontains'],'description':['icontains'],'lanes__pool__name':['icontains'],'lanes__pool__library__sample__id':['exact'],'lanes__pool__id':['exact']}#,'lanes__pool__library__name':['icontains'],'lanes__pool__name':['icontains']
    queryset = Run.objects.all()
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers.keys():
                return self.action_serializers[self.action]
        return viewsets.ModelViewSet.get_serializer_class(self)

class MachineViewSet(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    model = Machine
    filter_fields = {'name':['icontains'],'description':['icontains']}
#     filter_fields = {'machine__name':['icontains'],'description':['icontains']}#,'lanes__pool__library__name':['icontains'],'lanes__pool__name':['icontains']
    queryset = Machine.objects.all()
