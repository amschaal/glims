from django.conf import settings
from plugins import BasePlugin
from glims.models import Project
from django.conf.urls import url, include
import json

class LoggerPlugin(BasePlugin):
    id = 'logger-plugin' #Name of directive
    name = 'Logger Plugin'
    description = 'Plugin for creating change logs'
    js_files = ['logger/js/resources/models.js','logger/js/directives/logger.js']
    allowed_models = [Project]
    urls = url(r'^logger/', include('logger.urls'))
    @staticmethod
    def get_template(obj):
        types = json.dumps({key:value for key,value in settings.ACCOUNT_TYPES})
        return '<object-logs object-id="object_id" content-type="content_type"></object-logs>'
    @staticmethod
    def get_header_template(obj):
        return 'Logs'

