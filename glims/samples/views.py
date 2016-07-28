import csv
from django.http.response import HttpResponse
from extensible.models import ModelType
from glims.models import Project, Sample
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from glims.forms import SampleForm, FullSampleForm
from glims.api.serializers import SampleSerializer
from rest_framework import status
from django.db import transaction 
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.template.context import RequestContext
from glims.forms import FullSampleForm


def generate_template_rows(model_type):
    rows = []
    rows.append(['#'+model_type.name+': '+model_type.description])
    for field in model_type.fields:
        field_description = "#%s: %s" % (field['name'],field['label'])
        if field.has_key('help_text'):
            field_description += ", Description: %s" % field['help_text']
        if field.has_key('choices'):
            field_description += ", options: %s" % ', '.join([option['name'] for option in field['choices']])
        rows.append([field_description])
    headers = ['sample_id','name','description','received']
    if model_type:
        if model_type.fields:
            headers = headers + ['data.'+field['name'] for field in model_type.fields]#     field_names = [field.name for field in opts.fields]
    rows.append(headers)
    return rows
            
            
def sample_template_tsv(request):
    type_id = request.GET.get('type_id',False)
    print "TYPE" + type_id
    model_type = None if not type_id else ModelType.objects.get(pk=type_id)
    response = HttpResponse(content_type='text/tsv')
    response['Content-Disposition'] = 'attachment;filename=sample_template.tsv'
    # the csv writer
    writer = csv.writer(response,delimiter='\t')
    writer.writerows(generate_template_rows(model_type))
    return response

def sample_sheet_tsv(request,project_id):
    project = Project.objects.get(id=project_id)
    response = HttpResponse(content_type='text/tsv')
    response['Content-Disposition'] = 'attachment;filename=samplesheet.tsv'
    # the csv writer
    writer = csv.writer(response,delimiter='\t')
    writer.writerows(generate_template_rows(project.sample_type))
    for s in Sample.objects.filter(project=project):
        row = [s.sample_id,s.name,s.description,s.received]
        for field in project.sample_type.fields:
            row.append(s.data.get(field['name'],''))
        writer.writerow(row)
    return response

@api_view(['POST'])
@transaction.atomic
def import_samplesheet(request, project_id):
    sid = transaction.savepoint()
    try:
        project = Project.objects.get(pk=project_id)
        
        # the csv writer
#         dialect = csv.Sniffer().sniff(request.FILES['tsv'].read(1024),"\t")
#         request.FILES['tsv'].seek(0)
#         reader = csv.reader(request.FILES['tsv'], delimiter=dialect.delimiter)
        
        reader = csv.reader(request.FILES['tsv'],delimiter='\t')
        tsv = list(reader)
        for i, row in enumerate(tsv):
            if ''.join(row).strip().startswith('#'):
                continue
            else:
                start = i
                headers = row
                break
        values = [dict(zip(headers,sample)) for sample in tsv[start+1:]]
        errors = {}
        samples = []
        for index, row in enumerate(values): 
            sample_id =  row.get('sample_id',None)
            instance = None
            if sample_id:
                instance = Sample.objects.filter(sample_id = row.get('sample_id'), project=project).first()
            row['project']=project.id
            row['type'] = project.sample_type_id
            if instance:
                form = FullSampleForm(row,instance=instance)
            else:
                form = FullSampleForm(row)
            if form.is_valid():
                sample = form.save()
                samples.append(sample)
            else:
                print row
                for e in form.errors:
                    print e
                errors['row %d' % index] = form.errors
            print 'end loop'
        if len(errors.keys()) > 0:
            transaction.savepoint_rollback(sid)
            return Response({'errors':errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            transaction.savepoint_commit(sid)
            return Response([SampleSerializer(s).data for s in samples])
    except Exception, e:
        print e
        return Response({'errors':[]},status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def create_update_sample(request):
#     id = request.data.get('id',False)
#     if id:
#         instance = Sample.objects.get(id=id)
#         print instance
#         form = FullSampleForm(request.data,instance=instance)
#     else:
#         form = FullSampleForm(request.data)
#     if form.is_valid():
#         print 
#         sample = form.save()
#         return Response(SampleSerializer(sample).data)
#     else:
#         return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
#     
# class SampleUpdate(UpdateView):
#     template_name = 'glims/create_sample.html'
#     model = Sample
#     form_class = FullSampleForm
#     
# @login_required
# def create_sample(request):
#     if request.method == 'GET':
#         form = FullSampleForm()
#     elif request.method == 'POST':
#         form = FullSampleForm(request.POST)
#         if form.is_valid():
#             sample = form.save()
#             return redirect(sample.get_absolute_url()) 
#     return render(request, 'glims/create_sample.html', {'form':form} ,context_instance=RequestContext(request))
