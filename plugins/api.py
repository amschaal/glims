from rest_framework.decorators import api_view
from glims.plugin_classes import NotePlugin, FilePlugin, URLPlugin, SamplePlugin
from rest_framework.response import Response
from plugins.utils import get_available_plugins, PluginManager
from extensible.models import ModelType
from plugins.serializers import PluginSerializer
from plugins.models import ModelTypePlugin
from django.contrib.contenttypes.models import ContentType

@api_view(['GET'])
def get_plugins(request):
    plugins = []
    for p in [SamplePlugin,NotePlugin,FilePlugin,URLPlugin]:
        plugins.append({'header':p.get_header_template(None),'template':p.get_template(None)})
    return Response(plugins)

@api_view(['GET'])
def available_model_type_plugins(request,pk):
    model_type = ModelType.objects.get(pk=pk)
    available = get_available_plugins(model_type.content_type_id)
    return Response([PluginSerializer(plugin.get_instance()).data for plugin in available])

@api_view(['GET'])
def object_plugins(request,pk,content_type):
    ct = ContentType.objects.get(id=content_type)
    ct_class = ct.model_class()
    instance = ct_class.objects.get(pk=pk)
    plugins = []
    manager = PluginManager()
    configured_plugins = ModelTypePlugin.objects.filter(type=instance.type).order_by('order')
    for plugin in manager.get_model_plugins(ct_class):
        plugins.append({'header':plugin.get_header_template(instance),'template':plugin.get_template(instance)})
#     for p in [SamplePlugin,NotePlugin,FilePlugin,URLPlugin]:
    for p in configured_plugins:
        plugin = manager.get_plugin(p.plugin_id)
        plugins.append({'header':plugin.get_header_template(instance),'template':plugin.get_template(instance)})
    return Response(plugins)
#     
#     model_type = ModelType.objects.get(pk=pk)
#     available = get_available_plugins(model_type.content_type_id)
#     return Response([PluginSerializer(plugin.get_instance()).data for plugin in available])
