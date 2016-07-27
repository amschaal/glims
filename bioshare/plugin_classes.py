from plugins import BasePlugin
from glims.lims import Project

class BioshareProjectPlugin(BasePlugin):
    id = 'bioshare-project-plugin' #Name of directive
    name = 'Bioshare Project Plugin'
    description = 'Share project data via Bioshare'
    js_files = ['bioshare/js/resources/models.js','bioshare/js/directives/bioshare.js']
    models = [Project]
#     urls = url(r'^accounts/', include('accounts.urls'))
    @staticmethod
    def get_template(obj):
        return '<project-share project="project" ng-if="project.id"></project-share>'
    @staticmethod
    def get_header_template(obj):
        return 'Bioshare'

