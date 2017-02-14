from django.http.response import HttpResponse
from extensible.models import ModelType
from glims.models import Sample, Library, Pool
from rest_framework.response import Response
# from glims.forms import SampleForm, FullSampleForm
from glims.api.serializers import SampleSerializer, PoolSerializer
from rest_framework import status
from django.db import transaction 
import tablib
import copy
from django.utils import timezone

class Export(object):
    content_types = {'xls':'application/vnd.ms-excel','csv':'text/csv','json':'text/json'}
    headers = []
    def __init__(self,type=None):
        self.type = type if isinstance(type,ModelType) else ModelType.objects.filter(id=type).first()
        print self.type
    def prepare_row(self,row):
        data = {}
        #get rid of empty values
        for key in row.keys():
            if row[key] == '':
                row.pop(key)
        for key,val in row.iteritems():
            if key.startswith('data.'):
                data[key[5:]]=val
                del row[key]
        row['data'] = data
        return row
    def generate_headers(self):
        headers = copy.copy(self.headers)
        if self.type:
            if self.type.fields:
                headers += ['data.'+field['name'] for field in self.type.fields]#     field_names = [field.name for field in opts.fields]
        return headers
    def add_datetime_extension(self,filename):
        return "%s_%s"%(filename,timezone.now().strftime("%Y_%m_%d__%H_%M"))
    def response(self,request, dataset, filename, file_type="xls"):
        response_kwargs = {
            'content_type': Export.content_types[file_type]
        }
        filename = "%s.%s" %(filename,file_type)
        response = HttpResponse(getattr(dataset, file_type), **response_kwargs)
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
class ProjectExport(Export):
    """
    <tr><th>Status</th><td><resource-field-select resource="project" field="status" options="project.status_options" order-by-field="order"></resource-field-select></td></tr>
    <tr><th>ID</th><td>{[project.project_id]}</td></tr>
    <tr><th>Type</th><td>{[project.type.name]}</td></tr>
    <tr><th>Group</th><td>{[project.group.name]}</td></tr>
    <tr><th>Lab</th><td>{[project.lab.name]}</td></tr>
    <tr><th>Sample Type</th><td>{[project.sample_type.name]}</td></tr>
    <tr><th>Manager</th><td>{[ project.manager.first_name ]} {[ project.manager.last_name ]}</td></tr>
    <tr><th>Participants</th><td><span ng-repeat="user in project.participants">{[ user.first_name ]} {[ user.last_name ]}{[$last ? '' : ', ']}</span></td></tr>
    <tr><th>Description</th><td style="white-space: pre-wrap;">{[project.description]}</td></tr>
    <tr><th>Contact</th><td style="white-space: pre-wrap;">{[project.contact]}</td></tr>
    <tr><th>Related Projects</th><td><span ng-repeat="p in project.related_projects"><a title="Group: {[p.group__name]}, Lab: {[p.lab__name]}" href="{[getURL('project',{pk:p.id})]}">{[p.name]}</a>{[$last ? '' : ', ']}</span></td
    """
    headers = ['Id','Name','Type','Status','Group','Lab','Sample Type','Manager','Participants','Description','Contact','Related Projects','Created']
    def export(self,request,projects,filename_base='projects',file_type='xls',add_time_extension=True):
#         print self.generate_headers()
        data = tablib.Dataset(headers=self.generate_headers()) 
        for p in projects:
            row = [p.project_id,p.name,str(p.type),str(p.status),str(p.group),str(p.lab),str(p.sample_type),p.manager.name if p.manager else '',', '.join(u.name for u in p.participants.all()),p.description,p.contact,', '.join(proj.name for proj in p.related_projects.all()),p.created]
            for field in p.type.fields:
                row.append(p.data.get(field['name'],''))
            print row
            data.append(row)
        if add_time_extension:
            filename_base = self.add_datetime_extension(filename_base)
        return self.response(request,data,filename_base,file_type)
class SampleImportExport(Export):
    headers = ['sample_id','name','description','received','adapter','barcode','pool']
    def sample_template(self,request,filename_base='samplesheet_template',file_type='xls'):
        data = tablib.Dataset(headers=self.generate_headers())
        return self.response(request,data,filename_base,file_type)
    def sample_sheet(self,request,project,filename_base='samplesheet',file_type='xls'):
        data = tablib.Dataset(headers=self.generate_headers())
        for s in Sample.objects.filter(project=project):
            row = [s.sample_id,s.name,s.description,s.received,'','','']
            for field in project.sample_type.fields:
                row.append(s.data.get(field['name'],''))
            data.append(row)
        return self.response(request,data,filename_base,file_type)
    def import_samplesheet(self,request,file_handle,project):
        sid = transaction.savepoint()
        data = tablib.Dataset().load(file_handle.read())
        
        #initialize variables
        errors = {}
        samples = []
        pools = {}
        
        for index, row in enumerate(data.dict): 
            print index
            print row
            row = self.prepare_row(row)
            
            #If an autogenerated sample_id is listed, get the sample to update it            
            sample_id =  row.get('sample_id',None)
            instance = None
            if sample_id:
                instance = Sample.objects.filter(sample_id = row.get('sample_id'), project=project).first()
            
            row['project']=project.id
            row['type'] = project.sample_type_id
            if instance:
                sample = SampleSerializer(data=row,instance=instance,model_type=project.sample_type_id)
            else:
                sample = SampleSerializer(data=row,model_type=project.sample_type_id)
            if sample.is_valid():
                sample_instance = sample.save()
                samples.append(sample)
                #Keep track of pool name, if provided 
                pool = row.get('pool','')
                if not instance:
                    #Make a library
                    library = Library.objects.create(sample=sample_instance) #should include adapter and pool != '':
                    #Mark the library for addition to the given pool 
                    if pool != '':
                        if not pools.has_key(pool):
                            pools[pool] = []
                        pools[pool].append(library)
            else:
                sample_errors = dict(sample.errors)
                data_errors = sample_errors.pop('data',{})
                for field,field_errors in data_errors.iteritems():
                    sample_errors['data.%s'%field]=field_errors
                errors['row %d' % index] = sample_errors
            print 'end loop'
        
        #Create pools when necessary and add libraries
        for pool_name, libraries in pools.iteritems():
#             pool_name = '%s_%s'%(pool_name,project.project_id)
            #Check if the project has a pool of this name
            pool = Pool.objects.filter(libraries__sample__project=project,name=pool_name).first()
            #Create a new pool
            if not pool:
                pool_serializer = PoolSerializer(data={'name':pool_name,'group':project.group})
                if pool_serializer.is_valid():
                    pool = pool_serializer.save()
                else:
                    errors['Error creating pool "%s"'%pool_name] = pool_serializer.errors
                    continue
            #Add libraries
            pool.libraries.add(*libraries)
            pool.save()
            duplicates = pool.get_barcode_duplicates()
            if duplicates:
                errors['%s barcode duplicates' % pool.name] = {barcode:[', '.join(libraries)] for barcode,libraries in duplicates.iteritems()}
        if len(errors.keys()) > 0:
            transaction.savepoint_rollback(sid)
            return Response({'errors':errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            transaction.savepoint_commit(sid)
            return Response([s.data for s in samples])
