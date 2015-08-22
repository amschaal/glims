import csv
from django.http.response import HttpResponse
from extensible.models import ModelType
from glims.lims import Project, Sample
from rest_framework.decorators import api_view
from rest_framework.response import Response
from glims.forms import SampleForm
from glims.serializers import SampleSerializer
from rest_framework import status
from django.db import transaction 

def sample_template_tsv(request):
    type_id = request.GET.get('type_id',False)
    print "TYPE" + type_id
    model_type = None if not type_id else ModelType.objects.get(pk=type_id)
    response = HttpResponse(content_type='text/tsv')
    response['Content-Disposition'] = 'attachment;filename=sample_template.tsv'
    # the csv writer
    writer = csv.writer(response)
    writer.writerow([model_type.name+': '+model_type.description])
    headers = ['sample_id','name','description','received']
    if model_type:
        if model_type.fields:
            headers = headers + ['data__'+field['name'] for field in model_type.fields]#     field_names = [field.name for field in opts.fields]
    writer.writerow(headers)
#     # Write a first row with header information
#     writer.writerow(field_names)
#     # Write data rows
#     for obj in queryset:
#         writer.writerow([getattr(obj, field) for field in field_names])
    return response

@api_view(['POST'])
@transaction.atomic
def import_tsv_samples(request, project_id):
    sid = transaction.savepoint()
    try:
        project = Project.objects.get(pk=project_id)
        
        # the csv writer
        reader = csv.reader(request.FILES['tsv'],delimiter='\t')
        tsv = list(reader)
        headers = tsv[1]
        values = [dict(zip(headers,sample)) for sample in tsv[2:]]
        errors = {}
        samples = []
        for row in values:
            print row
            if row.get('sample_id',False):
                row['project']=project.id
                row['type'] = project.sample_type_id
                print row
                form = SampleForm(row)
                if form.is_valid():
                    sample = form.save()
                    print sample
                    samples.append(sample)
                else:
                    print 'error'
                    print form.errors
                    errors[row['sample_id']] = form.errors
        if len(errors.keys()) > 0:
            transaction.savepoint_rollback(sid)
            return Response({'errors':errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            transaction.savepoint_commit(sid)
            return Response([SampleSerializer(s).data for s in samples])
    except Exception, e:
        return Response({'errors':[]},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def create_update_sample(request):
    id = request.DATA.get('id',False)
    if id:
        instance = Sample.objects.get(id=id)
        form = SampleForm(request.DATA,instance=instance)
    else:
        form = SampleForm(request.DATA)
    if form.is_valid():
        sample = form.save()
        return Response(SampleSerializer(sample).data)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
