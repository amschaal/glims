from glims.models import Project
from rest_framework.decorators import api_view
# from glims.forms import SampleForm, FullSampleForm
from django.db import transaction 
from glims.samples.importer import SampleImportExport

def sample_template(request):
    type_id = request.GET.get('type_id',None)
    exporter = SampleImportExport(type=type_id)
    return exporter.sample_template(request, 'template', 'xls')

def sample_sheet(request,project_id):
    project = Project.objects.get(id=project_id)
    exporter = SampleImportExport(type=project.sample_type)
    return exporter.sample_sheet(request, project, 'samplesheet', 'xls')

@api_view(['POST'])
@transaction.atomic
def import_samplesheet(request, project_id):
    project = Project.objects.get(pk=project_id)
    exporter = SampleImportExport(type=project.sample_type)
    return exporter.import_samplesheet(request, request.FILES['sheet'], project)
    
