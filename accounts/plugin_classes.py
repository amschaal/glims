from django.conf import settings
from plugins import BasePlugin
from glims.lims import Project
from django.conf.urls import url, include


class AccountsPlugin(BasePlugin):
    id = 'account-plugin' #Name of directive
    name = 'Accounts Plugin'
    description = 'Manage project accounts'
    js_files = ['accounts/js/resources/models.js','accounts/js/directives/accounts.js']
    allowed_models = [Project]
    urls = url(r'^accounts/', include('accounts.urls'))
#     def get_attributes(self, obj):
#         return {'project':'project', 'ng-if':'project.id'}
    @staticmethod
    def get_template(obj):
        return '<project-accounts project-id="project.id"></project-accounts>'
    @staticmethod
    def get_header_template(obj):
        return 'Accounts ({[accounts_count]})'

