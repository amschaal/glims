from rest_framework.decorators import api_view
from glims.plugin_classes import NotePlugin, FilePlugin, URLPlugin, SamplePlugin
from rest_framework.response import Response
from plugins.utils import get_available_plugins
from extensible.models import ModelType
from plugins.serializers import PluginSerializer

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
def model_type_plugins(request,pk):
    model_type = ModelType.objects.get(pk=pk)
    available = get_available_plugins(model_type.content_type_id)
    return Response([PluginSerializer(plugin.get_instance()).data for plugin in available])
