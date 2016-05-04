

class BasePlugin(object):
    css_files = []
    js_files = []
    allowed_models=[]
    @classmethod
    def get_content_types(cls):
        from django.contrib.contenttypes.models import ContentType
        return set(value for key,value in ContentType.objects.get_for_models(*cls.allowed_models).items())
    @classmethod
    def get_instance(cls):
        from plugins.models import Plugin
        return Plugin.objects.get(id=cls.id)