from django.conf import settings
from plugins import BasePlugin
from glims.models import Project
from django.conf.urls import url, include
import json
from tracker.models import Log

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
        statuses = json.dumps(dict(Log.STATUS_CHOICES))
        print statuses
        return '<tracker-logs project-id="project.id" statuses=\'%s\'></tracker>'%statuses
    @staticmethod
    def get_header_template(obj):
        return 'Time Tracker'

