from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import UpdateView, CreateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.views.generic.edit import UpdateView
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from permissions.manage import get_all_user_objects
from sendfile import sendfile
from forms import FastaFileForm, TandemForm
from proteomics.models import FastaFile, ParameterFile
# from glims.jobs import JobFactory, DRMAAJob, SGE, JobSubmission, SLURM
import subprocess, json, shutil, pickle, os
from django_compute.models import Job
from glims.api.views import FileBrowser

@login_required
def fasta_files(request):
    return render(request, 'proteomics/fasta_files.html', {} )


@login_required
@api_view(['POST'])
def create_fasta_from_url(request):
    print 'test'
    if request.method == 'POST':
        form = FastaFileForm(request.data)
    if form.is_valid():
        fasta = form.save()
        form.download_file()
        fasta.save()
        fasta.create_decoys()
        print fasta
    else:
        print form.errors
    return Response({"status": "success!"})

def fasta_file(request,pk):
    instance = get_object_or_404(FastaFile,id=pk)
    return render(request, 'proteomics/fasta_file.html', {'instance':instance} )
def view_fasta(request,pk):
    from proteomics.utils import create_reverse, concatenate_files
    from proteomics import CRAP_FILE
    instance = get_object_or_404(FastaFile,id=pk)
    response = HttpResponse(content_type='text')
    if request.GET.get('transform',None) == 'reverse':
        output = create_reverse(instance.file)
    elif request.GET.get('transform',None) == 'with_crap':
        crapfile = open(CRAP_FILE,'r')
        output = concatenate_files([instance.file,crapfile])
    elif request.GET.get('transform',None) == 'f_r_with_crap':
        crapfile = open(CRAP_FILE,'r')
        with_crap = concatenate_files([instance.file,crapfile])
        reverse = create_reverse(with_crap)
        output = concatenate_files([with_crap,reverse])
    else:
        output = instance.file
    response.write(output.read())
    return response
    
class FastaFileCreate(CreateView):
    template_name = 'proteomics/create_fasta_file.html'
    model = FastaFile
    form_class = FastaFileForm
    success_url = reverse_lazy('proteomics__fasta_files')
    def form_valid(self, form):
        form.download_file()
        return super(FastaFileCreate, self).form_valid(form)
    
class FastaFileUpdate(UpdateView):
    template_name = 'proteomics/create_fasta_file.html'
    model = FastaFile
    form_class = FastaFileForm
    success_url = reverse_lazy('proteomics__fasta_files')
    def form_valid(self, form):
        form.download_file()
        return super(FastaFileUpdate, self).form_valid(form)

@login_required
def parameter_files(request):
    return render(request, 'proteomics/parameter_files.html', {} )

@login_required
def uniprot(request):
    return render(request, 'proteomics/uniprot.html', {} )

class ParameterFileCreate(CreateView):
    template_name = 'proteomics/create_parameter_file.html'
    model = ParameterFile
    success_url = reverse_lazy('proteomics__parameter_files')
    fields = ['file','type','name','description']
    def form_valid(self, form):
        parameter_file = form.save(commit=False)
        parameter_file.created_by = self.request.user
        parameter_file.save()
        return super(ParameterFileCreate, self).form_valid(form)

class ParameterFileUpdate(UpdateView):
    template_name = 'proteomics/create_parameter_file.html'
    model = ParameterFile
    success_url = reverse_lazy('proteomics__parameter_files')
    fields = ['file','type','name','description']

def searchcli(request):
#     from . import GENERATE_TANDEM_QSUB
#     print GENERATE_TANDEM_QSUB
#     if request.method == 'GET':
    form = TandemForm()
#     elif request.method == 'POST':
#         form = TandemForm(request.POST)
#         if form.is_valid():
#             print form.cleaned_data
#             args = ['http://google.com','http://yahoo.com']
#             job = JobFactory.create_job(SGE,**{'args':args,'name':'Tandem','path':'/var/www/virtualenv/glims/include/glims/proteomics/scripts/test.sh'})
#             job.run()
#             return redirect('proteomics__fasta_files') 
    return render(request, 'proteomics/searchcli.html', {'form':form} )


@api_view(['POST'])
def run_searchcli(request):
    print request.data
    from django.utils.crypto import get_random_string
    from rest_framework.response import Response
    
    
    from django_compute.models import JobTemplate
    from glims.callbacks import DataOutputtedCallback
    
    from proteomics import JOB_DIRECTORY, LOCAL_JOB_DIRECTORY, TANDEM_SCRIPT, SCAFFOLD_SCRIPT
    form = TandemForm(request.data)
    
    if form.is_valid():
        spectrum_files = []
        for sample in form.cleaned_data['samples']:
            if sample.data.has_key('mzml_path'):
                spectrum_files.append(sample.data['mzml_path'])
        if len(spectrum_files) ==0:
            raise Exception('No valid spectrum files were specified')
        import time
        directory = '/data/proteomics/jobs/%s' % get_random_string()
        if not os.path.exists(directory):
            os.makedirs(directory)
        script_path = os.path.join(directory,'searchcli.sh')
        searchcli = JobTemplate.objects.get(id='searchcli')
        fasta_file =  form.cleaned_data['fasta_file']
        job = Job.objects.create(
                script_path=script_path,
                output_directory=directory,
                params=
                    {'directory':directory,
                     'spectrum_files':','.join(spectrum_files),
                     'fasta_file':fasta_file.file.path,#form.cleaned_data['fasta_file'].file.path,
                     'parameter_file':form.cleaned_data['parameter_file'].file.path,
                     'engine':request.data['engine']
                    },
                callback_id=DataOutputtedCallback.id,
                template=searchcli
            )
        job.run()
        
        print form.cleaned_data
        return Response({'job_id':job.id})
        
    return Response({'errors':form.errors})

class MZMLBrowser(FileBrowser):
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAdminUser,)
    extension_filters = ['.mzml','.mzML']
    base_directory = '/tmp'