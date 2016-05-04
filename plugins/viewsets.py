from plugins.serializers import ModelTypePluginSerializer, PluginSerializer
from rest_framework import viewsets
from plugins.models import ModelTypePlugin, Plugin

class ModelTypePluginViewset(viewsets.ModelViewSet):
    model = ModelTypePlugin
    serializer_class = ModelTypePluginSerializer
    ordering_fields = ('order')
    filter_fields = {'type':['exact'],'plugin':['exact'],'id':['exact']}
    def get_queryset(self):
        return ModelTypePlugin.objects.all()

class PluginViewset(viewsets.ReadOnlyModelViewSet):
    model = Plugin
    serializer_class = PluginSerializer
#     filter_fields = {'type':['exact'],'plugin':['exact'],'id':['exact']}
    def get_queryset(self):
        return Plugin.objects.all()