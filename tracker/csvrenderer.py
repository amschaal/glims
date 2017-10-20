from django.utils.encoding import smart_unicode
from rest_framework import renderers
from rest_framework_csv.renderers import CSVRenderer

class SimpleCSVRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'csv'

    def render(self, data, media_type=None, renderer_context=None):
        print 'render'
        print self
        print renderer_context
#         print data['results']
        string = ''
        for row in data['results']:
            print row.values()
            string += ",".join([str(val) for val in data.values()]) + '\n'
        return string.encode(self.charset)

class PaginatedCSVRenderer (CSVRenderer):
    results_field = 'results'
    header = ['modified','status','quantity','category.name','user.name','project.name','project.lab','description']
    labels = {
        'category.name': 'Category','user.name':'User','project.name':'Project','project.lab':'Lab'
    }
    def render(self, data, *args, **kwargs):
        if not isinstance(data, list):
            data = data.get(self.results_field, [])
        return super(PaginatedCSVRenderer, self).render(data, *args, **kwargs)
    
