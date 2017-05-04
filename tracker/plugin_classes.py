from django.conf import settings
from plugins import BasePlugin
from glims.models import Project
from django.conf.urls import url, include
import json

class TrackerLogPlugin(BasePlugin):
    id = 'tracker-logs' #Name of directive
    name = 'Tracker Log Plugin'
    description = 'Project time tracking'
    js_files = ['tracker/js/resources/models.js','tracker/js/directives/tracker.js']
    models = [Project]
    urls = url(r'^tracker/', include('tracker.urls'))
#     def get_attributes(self, obj):
#         return {'project':'project', 'ng-if':'project.id'}
    @staticmethod
    def get_template(obj):
#         types = json.dumps({key:value for key,value in settings.ACCOUNT_TYPES})
        return '<tracker-logs project-id="project.id"></tracker>'
    @staticmethod
    def get_header_template(obj):
        return 'Time Tracker'

