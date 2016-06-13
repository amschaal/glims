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
    
class PluginManager(object):
    def __init__(self):
        PLUGINS = getattr(settings,'PLUGINS')
        self.plugins = {}
        for plugin_string in PLUGINS:
            plugin = import_string(plugin_string)
            self.plugins[plugin.id] = plugin
    def get_plugin(self,id):
        return self.plugins[id]
    def get_urls(self):
        urls = []
        for plugin in self.plugins.values():
            if plugin.urls:
                urls.append(plugin.urls)
        return urls
            
        
