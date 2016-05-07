from glims.lims import Project, Sample, Pool
from django.conf import settings
from plugins import BasePlugin

class SamplePlugin(BasePlugin):
    id = 'samples-plugin' #Name of directive
    name = 'Samples Plugin'
    description = 'Allows management of project samples'
#     template = 'glims/plugins/manage_samples.html'
    css_files = ['vendor/ui-grid/ui-grid.min.css']
    js_files = ['vendor/ui-grid/ui-grid.min.js','js/directives/samples.plugin.js']
    allowed_models = [Project]
    def get_attributes(self, obj):
        return {'project':'project', 'ng-if':'project.id'}
    @staticmethod
    def get_template(obj):
        return '<samples-plugin project="project"></samples-plugin>'
    @staticmethod
    def get_header_template(obj):
        return 'Samples ({[sample_count]})'
#     extra_context = {'BASE_URL':settings.BASE_URL,'foo':'bar'} #to be passed to template

class NotePlugin(BasePlugin):
    id = 'attachment-notes'
    name = 'Note Plugin'
    description = 'Allows addition of notes'
#     template = 'glims/plugins/notes.html'
    js_files = ['attachments/js/resources/models.js','attachments/js/directives/notes.js']
    css_files = ['attachments/css/attachments.css']
    @staticmethod
    def get_template(obj):
        return '<attachment-notes object-id="object_id" content-type="content_type"></attachment-notes>'
    @staticmethod
    def get_header_template(obj):
        return 'Notes ({[attachments_object.notes]})'
    #
    allowed_models = [Project,Sample,Pool]
class URLPlugin(BasePlugin):
    id = 'url-plugin'
    name = 'URL Plugin'
    description = 'Allows addition of urls'
#     template = 'glims/plugins/notes.html'
    js_files = ['attachments/js/resources/models.js','attachments/js/directives/urls.js']
    css_files = ['attachments/css/attachments.css']
    @staticmethod
    def get_template(obj):
        return '<attachment-urls object-id="object_id" content-type="content_type"></attachment-notes>'
    @staticmethod
    def get_header_template(obj):
        return 'URLs ({[attachments_object.urls]})'
    allowed_models = [Project,Sample,Pool]
class FilePlugin(BasePlugin):
    id = 'file-plugin'
    name = 'File Plugin'
    description = 'Allows addition of files'
#     template = 'glims/plugins/notes.html'
    js_files = ['attachments/js/resources/models.js','attachments/js/vendor/ng-file-upload/ng-file-upload-shim.min.js','attachments/js/vendor/ng-file-upload/ng-file-upload.min.js','attachments/js/directives/files.js']
    css_files = ['attachments/css/attachments.css']
    allowed_models = [Project,Sample,Pool]
    @staticmethod
    def get_template(obj):
        return '<attachment-files object-id="object_id" content-type="content_type"></attachment-files>'
    @staticmethod
    def get_header_template(obj):
        return 'Files ({[attachments_object.files]})'
    

"""
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
