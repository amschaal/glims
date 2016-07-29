from django.conf import settings
from plugins import BasePlugin
from glims.models import Project
from django.conf.urls import url, include
import json

class AccountsPlugin(BasePlugin):
    id = 'account-plugin' #Name of directive
    name = 'Accounts Plugin'
    description = 'Manage project accounts'
    js_files = ['accounts/js/resources/models.js','accounts/js/directives/accounts.js']
    models = [Project]
    urls = url(r'^accounts/', include('accounts.urls'))
#     def get_attributes(self, obj):
#         return {'project':'project', 'ng-if':'project.id'}
    @staticmethod
    def get_template(obj):
        types = json.dumps({key:value for key,value in settings.ACCOUNT_TYPES})
        return '<project-accounts project-id="project.id" types=\'%s\'></project-accounts>'%(types)
    @staticmethod
    def get_header_template(obj):
        return 'Accounts ({[accounts_count]})'

