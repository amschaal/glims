from glims.lims import Project, Sample, Pool
from django.conf import settings




class SamplePlugin(object):
    id = 'sample-plugin' #Name of directive
    name = 'Sample Plugin'
    description = 'Allows management of project samples'
#     template = 'glims/plugins/manage_samples.html'
    css_files = ['vendor/ui-grid/ui-grid.min.css']
    js_files = ['vendor/ui-grid/ui-grid.min.js']
    allowed_models = [Project]
#     extra_context = {'BASE_URL':settings.BASE_URL,'foo':'bar'} #to be passed to template
"""
class NotePlugin(object):
    id = 'note-plugin'
    name = 'Note Plugin'
    description = 'Allows addition of notes'
#     template = 'glims/plugins/notes.html'
    js_files = ['attachments/static/attachments/js/pages/notes.js']
    css_files = ['attachments/static/attachments/css/attachments.js','sdfsdf']
    allowed_models = [Project,Sample,Pool]

class BiosharePlugin(object):
    id = 'bioshare_plugin'
    name = 'Bioshare plugin'
    description = 'Allow user to view bioshare files'
#     template = 'glims/plugins/notes.html'
    allowed_models = [Project,Sample,Pool]
    @staticmethod
    def initialize_request(request):
        pass
        #get session JWT token if not exists
        #set session JWT token
        
#in settings.py
# PLUGINS = [SamplePlugin,BiosharePlugin,NotePlugin]
"""
