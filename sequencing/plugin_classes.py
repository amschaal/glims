from glims.models import Pool, Sample
from django.conf import settings
from plugins import BasePlugin

class PoolRunsPlugin(BasePlugin):
    id = 'pool-runs-plugin' #Name of directive
    name = 'Pool Runs Plugin'
    description = 'Show sequencing runs for a pool'
    js_files = ['sequencing/js/resources/models.js','sequencing/js/directives/sequencing_runs.plugin.js']
    models = [Pool]
    @staticmethod
    def get_template(obj):
        return '<sequencing-runs pool="pool"></sequencing-runs>'
    @staticmethod
    def get_header_template(obj):
        return 'Sequencing Runs ({[run_count]})'

class SampleRunsPlugin(BasePlugin):
    id = 'sample-runs-plugin' #Name of directive
    name = 'Sample Runs Plugin'
    description = 'Show sequencing runs for a samle'
    js_files = ['sequencing/js/resources/models.js','sequencing/js/directives/sequencing_runs.plugin.js']
    models = [Sample]
    @staticmethod
    def get_template(obj):
        return '<sequencing-runs sample="sample"></sequencing-runs>'
    @staticmethod
    def get_header_template(obj):
        return 'Sequencing Runs ({[run_count]})'