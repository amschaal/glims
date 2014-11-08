from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.db.models import Q
from lims import *
from django.contrib.auth.decorators import login_required
from permissions.manage import get_all_user_objects
from sendfile import sendfile
from forms import FileForm, StudyForm, ExperimentForm, SampleForm
import json

# @login_required
def home(request):
    return render(request, 'glims/dashboard.html', {},context_instance=RequestContext(request))
def study(request, pk):
    study = Study.objects.get(pk=pk)
#     ct = ContentType.objects.get_for_model(study)
    return render(request, 'glims/study.html', {'study':study} ,context_instance=RequestContext(request))
def sample(request,pk):
    sample = Sample.objects.get(pk=pk)
    return render(request, 'glims/sample.html', {'sample':sample} ,context_instance=RequestContext(request))
def experiment(request,pk):
    experiment = Experiment.objects.get(pk=pk)
    return render(request, 'glims/experiment.html', {'experiment':experiment} ,context_instance=RequestContext(request))
def pis(request):
    return render(request, 'glims/pis.html', {} ,context_instance=RequestContext(request))
def studies(request):
#     studies = get_all_user_objects(request.user, ['view'], Study)#Study.objects.all()
    query = json.dumps(request.GET)
    return render(request, 'glims/studies.html', {'query':query} ,context_instance=RequestContext(request))
def samples(request):
    query = json.dumps(request.GET)
#     samples = get_all_user_objects(request.user, ['view'], Sample)#Sample.objects.all()
    return render(request, 'glims/samples.html', {'query':query} ,context_instance=RequestContext(request))
def experiments(request):
    query = json.dumps(request.GET)
#     experiments = get_all_user_objects(request.user, ['view'], Experiment)#Experiment.objects.all()
    return render(request, 'glims/experiments.html', {'query':query} ,context_instance=RequestContext(request))

def create_study(request):
    if request.method == 'GET':
        form = StudyForm()
    elif request.method == 'POST':
        form = StudyForm(request.POST)
        if form.is_valid():
            study = form.save()
            return redirect(study.get_absolute_url()) 
    return render(request, 'glims/create_study.html', {'form':form} ,context_instance=RequestContext(request))

def create_sample(request):
    if request.method == 'GET':
        form = SampleForm()
    elif request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            sample = form.save()
            return redirect(sample.get_absolute_url()) 
    return render(request, 'glims/create_sample.html', {'form':form} ,context_instance=RequestContext(request))

def create_experiment(request):
    if request.method == 'GET':
        form = ExperimentForm()
    elif request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            experiment = form.save()
            return redirect(experiment.get_absolute_url()) 
    return render(request, 'glims/create_experiment.html', {'form':form} ,context_instance=RequestContext(request))

class SampleUpdate(UpdateView):
    template_name = 'glims/create_sample.html'
    model = Sample

def get_file(request,pk):
    file = File.objects.get(id=pk)
    return sendfile(request, file.file.path)
def attach_file(request,model,pk):
    ct = ContentType.objects.get(model=model)
    klass = ct.model_class()
    obj = klass.objects.get(pk=pk)
    next = request.REQUEST.get('next',request.META['HTTP_REFERER'])
    if request.method == 'GET':
        form = FileForm()
    elif request.method == 'POST':
        form = FileForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploaded_by=request.user
            obj.object_id = pk
            obj.content_type = ct
            obj.save()
            return redirect(next)
    return render(request, 'glims/attach_file.html', {'form':form, 'obj': obj, 'next':next} ,context_instance=RequestContext(request))
            
            