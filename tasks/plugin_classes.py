from glims.lims import Project, Sample, Pool
from django.conf import settings
from plugins import BasePlugin
    
class TasksPlugin(BasePlugin):
    id = 'tasks-plugin'
    name = 'Tasks Plugin'
    description = 'Show tasks'
    js_files = ['tasks/vendor/angular-moment/moment.js',
                'tasks/vendor/angular-moment/angular-moment.min.js',
                'tasks/vendor/angular-gantt/angular-gantt.min.js',
                'tasks/vendor/angular-gantt/angular-gantt-plugins.min.js',
                'tasks/js/directives/tasks.js',
                'tasks/js/resources/task.js',]
    css_files = ['tasks/vendor/angular-gantt/angular-gantt.min.css','tasks/vendor/angular-gantt/angular-gantt-plugins.min.css']
    allowed_models = [Project,Sample,Pool]
    @staticmethod
    def get_template(obj):
        return '<tasks-plugin object-id="object_id" content-type="content_type"></tasks-plugin>'
    @staticmethod
    def get_header_template(obj):
        return 'Tasks'
