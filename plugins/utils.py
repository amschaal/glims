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
        self.model_plugins = {}
        for plugin_string in PLUGINS:
            plugin = import_string(plugin_string)
            self.plugins[plugin.get_id()] = plugin
            for model in plugin.models:
                if not self.model_plugins.has_key(model.__name__):
                    self.model_plugins[model.__name__] = [plugin] 
                else:
                    self.model_plugins[model.__name__] += [plugin]
    def get_plugins(self):
        return self.plugins.items()
    def get_plugin(self,id):
        return self.plugins[id]
    def get_model_plugins(self,model):
        if self.model_plugins.has_key(model.__name__):
            return self.model_plugins[model.__name__]
        else:
            return []
#     def get_plugins_by_class(self,klass):
#         
    def get_urls(self):
        """
        Return all the URLs for configured plugins.  For use in main URL config file.
        plugin_manager = PluginManager()
        urlpatterns += plugin_manager.get_urls()
        """
        urls = []
        for plugin in self.plugins.values():
            if plugin.urls:
                urls.append(plugin.urls)
        return urls
            
        
