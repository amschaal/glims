from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from lims import *
from django.contrib.auth.decorators import login_required
from permissions.manage import get_all_user_objects
from sendfile import sendfile
from forms import ProjectForm, ExperimentForm, SampleForm, CreateWorkflowForm, WorkflowForm, ProcessForm#, FileForm
import json

@login_required
def home(request):
    return render(request, 'glims/dashboard.html', {},context_instance=RequestContext(request))
@login_required
def project(request, pk):
    project = Project.objects.get(pk=pk)
    inlines = ModelTypePlugins.objects.filter(type=project.type,layout=ModelTypePlugins.INLINE_LAYOUT, plugin__page='project').order_by('weight')
    tabs = ModelTypePlugins.objects.filter(type=project.type,layout=ModelTypePlugins.TABBED_LAYOUT, plugin__page='project').order_by('weight')
    return render(request, 'glims/project.html', {'project':project,'inlines':inlines,'tabs':tabs} ,context_instance=RequestContext(request))
@login_required
def sample(request,pk):
    sample = Sample.objects.get(pk=pk)
    inlines = ModelTypePlugins.objects.filter(type=sample.type,layout=ModelTypePlugins.INLINE_LAYOUT, plugin__page='sample').order_by('weight')
    tabs = ModelTypePlugins.objects.filter(type=sample.type,layout=ModelTypePlugins.TABBED_LAYOUT, plugin__page='sample').order_by('weight')
    return render(request, 'glims/sample.html', {'sample':sample,'inlines':inlines,'tabs':tabs} ,context_instance=RequestContext(request))
@login_required
def experiment(request,pk):
    experiment = Experiment.objects.get(pk=pk)
    plugins = experiment.sample.type.plugins.filter(page='experiment')
    return render(request, 'glims/experiment.html', {'experiment':experiment,'plugins':plugins} ,context_instance=RequestContext(request))
@login_required
def pis(request):
    return render(request, 'glims/pis.html', {} ,context_instance=RequestContext(request))
@login_required
def projects(request):
#     projects = get_all_user_objects(request.user, ['view'], Project)#Project.objects.all()
    query = json.dumps(request.GET)
    return render(request, 'glims/projects.html', {'query':query} ,context_instance=RequestContext(request))
@login_required
def samples(request):
    query = json.dumps(request.GET)
#     samples = get_all_user_objects(request.user, ['view'], Sample)#Sample.objects.all()
    return render(request, 'glims/samples.html', {'query':query} ,context_instance=RequestContext(request))
@login_required
def experiments(request):
    query = json.dumps(request.GET)
#     experiments = get_all_user_objects(request.user, ['view'], Experiment)#Experiment.objects.all()
    return render(request, 'glims/experiments.html', {'query':query} ,context_instance=RequestContext(request))
# @login_required
# def workflow(request):
#     return render(request, 'glims/workflow.html', {} ,context_instance=RequestContext(request))
@login_required
def model_types(request):
    content_types = ContentType.objects.all()
    return render(request, 'glims/model_types.html', {'content_types':content_types} ,context_instance=RequestContext(request))
@login_required
def create_project(request):
    if request.method == 'GET':
        form = ProjectForm()
    elif request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect(project.get_absolute_url()) 
    return render(request, 'glims/create_project.html', {'form':form} ,context_instance=RequestContext(request))
@login_required
def create_sample(request):
    if request.method == 'GET':
        form = SampleForm()
    elif request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            sample = form.save()
            return redirect(sample.get_absolute_url()) 
    return render(request, 'glims/create_sample.html', {'form':form} ,context_instance=RequestContext(request))
@login_required
def create_workflow(request):
    if request.method == 'GET':
        form = CreateWorkflowForm()
    elif request.method == 'POST':
        form = CreateWorkflowForm(request.POST)
        if form.is_valid():
            workflow = form.save()
            template = workflow.workflow_template
            workflow.type = template.type
            for process in template.processes.all():
                process = Process.objects.create(type=process,workflow=workflow)
            workflow.save()
            return redirect(workflow.get_absolute_url()) 
    return render(request, 'glims/create_workflow.html', {'form':form} ,context_instance=RequestContext(request))
@login_required
def workflow(request,pk):
    workflow = Workflow.objects.get(pk=pk)
#     plugins = workflow.plugins.filter(page='workflow')
    if request.POST.get('workflow',False):
        workflow_form = WorkflowForm(request.POST,instance=workflow)
        if workflow_form.is_valid():
            workflow_form.save()
    else:
        workflow_form = WorkflowForm(instance=workflow)
    processes = []
    
    for process in workflow.processes.all():
        print "%s:%s"%(request.POST.get('process_id'),process.id)
        if request.POST and request.POST.get('process_id','') == str(process.id):
            print "POST!!!!"
            form = ProcessForm(request.POST,instance=process)
            if form.is_valid():
                form.save()
            processes.append({'process':process, 'form':form, 'valid':form.is_valid(),'submitted':True})
        else:
            processes.append({'process':process, 'form':ProcessForm(instance=process)})
    return render(request, 'glims/workflow.html', {'workflow':workflow,'workflow_form':workflow_form,'processes':processes} ,context_instance=RequestContext(request))
# @login_required
# def update_process(request,pk):
#     process = Process.objects.get(pk=pk)
# #     plugins = workflow.plugins.filter(page='workflow')
#     process_form = WorkflowForm(instance=workflow)
#     processes = []
#     for process in workflow.processes.all():
#         processes.append({'process':process, 'form':ProcessForm(instance=process)})
#     return render(request, 'glims/workflow.html', {'workflow':workflow,'workflow_form':workflow_form,'processes':processes} ,context_instance=RequestContext(request))



class SampleUpdate(UpdateView):
    template_name = 'glims/create_sample.html'
    model = Sample
    form_class = SampleForm
class ProjectUpdate(UpdateView):
    template_name = 'glims/create_project.html'
    model = Project
    form_class = ProjectForm


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
            