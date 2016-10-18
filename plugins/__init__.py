

class BasePlugin(object):
    id = None # Must override this with a unique ID for the plugin
    css_files = [] # Required CSS files
    js_files = [] # Required JavaScript files
    allowed_models=[] # To which models should this plugin be made available
    models=[] # For which models will this plugin always be available
    urls = None # URLs to include.  Usually API calls of some sort.  IE: url(r'^my_plugin/', include('my_plugin.urls'))
    @classmethod
    def get_id(cls):
        if cls.id is None:
            raise Exception("All plugins must have an associated id.  Offending plugin is: %s"%cls.__name__)
        return cls.id
    @classmethod
    def get_content_types(cls):
        """
        Returns the set of content types for all models listed in allowed_models.
        """
        from django.contrib.contenttypes.models import ContentType
        return set(value for key,value in ContentType.objects.get_for_models(*cls.allowed_models).items())
    @classmethod
    def get_instance(cls):
        """
        Get a Plugin instance based on Model class.
        """
        from plugins.models import Plugin
        return Plugin.objects.get(id=cls.id)
    @staticmethod
    def get_template(obj):
        """
        Should return the angular template to be rendered.  This should often be as simple as a directive with a couple arguments.
        If a more complicated template is necessary, you can render a template passing the instance in as context.
        The rendered template will be the contents of the tab.
        """
        raise NotImplementedError()
    @staticmethod
    def get_header_template(obj):
        """
        This will be the header of the tab.  It can likewise contain directives.
        """
        raise NotImplementedError()