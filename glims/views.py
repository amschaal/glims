from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.db.models import Q
from lims import *
from django.contrib.auth.decorators import login_required
from permissions.manage import get_all_user_objects
from sendfile import sendfile
from forms import ProjectForm, ExperimentForm, SampleForm#, FileForm
import json

# @login_required
def home(request):
    return render(request, 'glims/dashboard.html', {},context_instance=RequestContext(request))
def project(request, pk):
    project = Project.objects.get(pk=pk)
    inlines = ProjectTypePlugins.objects.filter(type=project.type,layout=ProjectTypePlugins.INLINE_LAYOUT, plugin__page='project').order_by('weight')
    tabs = ProjectTypePlugins.objects.filter(type=project.type,layout=ProjectTypePlugins.TABBED_LAYOUT, plugin__page='project').order_by('weight')
    return render(request, 'glims/project.html', {'project':project,'inlines':inlines,'tabs':tabs} ,context_instance=RequestContext(request))
def sample(request,pk):
    sample = Sample.objects.get(pk=pk)
    inlines = ProjectTypePlugins.objects.filter(type=sample.project.type,layout=ProjectTypePlugins.INLINE_LAYOUT, plugin__page='sample').order_by('weight')
    tabs = ProjectTypePlugins.objects.filter(type=sample.project.type,layout=ProjectTypePlugins.TABBED_LAYOUT, plugin__page='sample').order_by('weight')
    return render(request, 'glims/sample.html', {'sample':sample,'inlines':inlines,'tabs':tabs} ,context_instance=RequestContext(request))
def experiment(request,pk):
    experiment = Experiment.objects.get(pk=pk)
    plugins = experiment.sample.project.type.plugins.filter(page='experiment')
    return render(request, 'glims/experiment.html', {'experiment':experiment,'plugins':plugins} ,context_instance=RequestContext(request))
def pis(request):
    return render(request, 'glims/pis.html', {} ,context_instance=RequestContext(request))
def projects(request):
#     projects = get_all_user_objects(request.user, ['view'], Project)#Project.objects.all()
    query = json.dumps(request.GET)
    return render(request, 'glims/projects.html', {'query':query} ,context_instance=RequestContext(request))
def samples(request):
    query = json.dumps(request.GET)
#     samples = get_all_user_objects(request.user, ['view'], Sample)#Sample.objects.all()
    return render(request, 'glims/samples.html', {'query':query} ,context_instance=RequestContext(request))
def experiments(request):
    query = json.dumps(request.GET)
#     experiments = get_all_user_objects(request.user, ['view'], Experiment)#Experiment.objects.all()
    return render(request, 'glims/experiments.html', {'query':query} ,context_instance=RequestContext(request))

def create_project(request):
    if request.method == 'GET':
        form = ProjectForm()
    elif request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect(project.get_absolute_url()) 
    return render(request, 'glims/create_project.html', {'form':form} ,context_instance=RequestContext(request))

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

"""
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
"""            
            