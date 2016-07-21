from django.conf import settings
from plugins import BasePlugin
from glims.lims import Project
from django.conf.urls import url, include
import json

class BioshareProjectPlugin(BasePlugin):
    id = 'bioshare-project-plugin' #Name of directive
    name = 'Bioshare Project Plugin'
    description = 'Share project data via Bioshare'
    js_files = ['bioshare/js/directives/bioshare.js']
    allowed_models = [Project]
#     urls = url(r'^accounts/', include('accounts.urls'))
#     def get_attributes(self, obj):
#         return {'project':'project', 'ng-if':'project.id'}
    @staticmethod
    def get_template(obj):
#         types = json.dumps({key:value for key,value in settings.ACCOUNT_TYPES})
        return '<bioshare-project project-id="project.id"></bioshare-project>'
    @staticmethod
    def get_header_template(obj):
        return 'Sharing'

