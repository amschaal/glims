from django.conf import settings
from django.utils.module_loading import import_string

def get_available_plugins(content_type_id):
    PLUGINS = getattr(settings,'PLUGINS')
    plugins = []
    for plugin_string in PLUGINS:
        plugin = import_string(plugin_string)
        print plugin_string
        print [ct for ct in plugin.get_content_types()]
        if content_type_id in [ct.pk for ct in plugin.get_content_types()]:
            plugins.append(plugin)
    return plugins
        
