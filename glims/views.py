from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from lims import *
from jobs import JobFactory, JobSubmission
from glims.serializers import SampleSerializer, PoolSerializer
from django.contrib.auth.decorators import login_required
from permissions.manage import get_all_user_objects
from sendfile import sendfile
from forms import ProjectForm, SampleForm, CreateWorkflowForm, WorkflowForm, ProcessForm, PoolForm, LabForm#, FileForm
import json
from angular_forms.decorators import AngularFormDecorator 
from glims.forms import ProjectTypeForm
from django_compute.models import Job

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
    pool_workflows = Workflow.objects.filter(pool__id__in=[pool['id'] for pool in sample.pools.all().values('id')])
    return render(request, 'glims/sample.html', {'sample':sample,'pool_workflows':pool_workflows,'inlines':inlines,'tabs':tabs} ,context_instance=RequestContext(request))
@login_required
def pool(request,pk):
    pool = Pool.objects.get(pk=pk)
#     samples = SampleSerializer(pool.samples.all()).data
    form = AngularFormDecorator(PoolForm)(instance=pool,prefix="pool")
    sample_form = AngularFormDecorator(PoolForm)(instance=pool,prefix="sample",field_template='glims/crispy/sample_field.html')
    return render(request, 'glims/pool.html', {'pool':pool,'form':form,'sample_form':sample_form} ,context_instance=RequestContext(request))
@login_required
def labs(request):
    return render(request, 'glims/labs.html', {} ,context_instance=RequestContext(request))
@login_required
def lab(request, pk):
    lab = Lab.objects.get(pk=pk)
#     inlines = ModelTypePlugins.objects.filter(type=project.type,layout=ModelTypePlugins.INLINE_LAYOUT, plugin__page='project').order_by('weight')
#     tabs = ModelTypePlugins.objects.filter(type=project.type,layout=ModelTypePlugins.TABBED_LAYOUT, plugin__page='project').order_by('weight')
    return render(request, 'glims/lab.html', {'lab':lab} ,context_instance=RequestContext(request))
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
def pools(request):
    return render(request, 'glims/pools.html', {} ,context_instance=RequestContext(request))
@login_required
def workflows(request):
    return render(request, 'glims/workflows.html', {} ,context_instance=RequestContext(request))
@login_required
def jobs(request):
    return render(request, 'glims/jobs.html', {} ,context_instance=RequestContext(request))
@login_required
def job(request,id):
    job = Job.objects.get(id=id)
    return render(request, 'glims/job.html', {'job':job} ,context_instance=RequestContext(request))
@login_required
def job_submission(request,id):
    submission = JobSubmission.objects.get(id=id)
    return render(request, 'glims/job_submission.html', {'submission':submission} ,context_instance=RequestContext(request))
@login_required
def cart(request):
    return render(request, 'glims/cart.html', {} ,context_instance=RequestContext(request))
@login_required
def model_types(request):
    content_types = ContentType.objects.all()
    return render(request, 'glims/model_types.html', {'content_types':content_types} ,context_instance=RequestContext(request))
@login_required
def model_type(request,pk):
    model_type = ModelType.objects.get(pk=pk)
    init = {'fields':model_type.fields,'name':model_type.name,'description':model_type.description,'content_type':model_type.content_type.id,'id':model_type.id,'urls':{'update':reverse('update_model_type',kwargs={"pk":pk})}}#{'update':reverse('update_model_type',kwargs={"pk":pk})}
    return render(request, 'glims/model_type.html', {'init':json.dumps(init),'model_type':model_type},context_instance=RequestContext(request))
#     return render(request, 'glims/model_type.html', {'job':job} ,context_instance=RequestContext(request))

@login_required
def create_lab(request):
    if request.method == 'GET':
        form = LabForm()
    elif request.method == 'POST':
        form = LabForm(request.POST)
        if form.is_valid():
            lab = form.save()
            return redirect(reverse('lab',kwargs={'pk':lab.pk})) 
    return render(request, 'glims/create_lab.html', {'form':form} ,context_instance=RequestContext(request))
@login_required
def choose_project_type(request):
    form = ProjectTypeForm(initial={'lab':request.GET.get('lab',None)})
    return render(request, 'glims/choose_project_type.html', {'form':form} ,context_instance=RequestContext(request))
@login_required
def create_project(request,pk=None):
    instance = None if not pk else Project.objects.get(pk=pk)
    initial = None if pk else {'lab':request.GET.get('lab',None),'type':request.GET.get('type',None)}
    if request.method == 'GET':
        form = ProjectForm(instance=instance,initial=initial)
    elif request.method == 'POST':
        form = ProjectForm(request.POST,instance=instance,initial=initial)
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
def create_pool(request):
    if request.method == 'GET':
        form = PoolForm()
    elif request.method == 'POST':
        form = PoolForm(request.POST)
        if form.is_valid():
            pool = form.save()
            sample_ids = request.session.get('sample_cart', [])
            pool.samples = Sample.objects.filter(pk__in=sample_ids)
            pool.save()
            return redirect(pool.get_absolute_url()) 
    return render(request, 'glims/create_pool.html', {'form':form} ,context_instance=RequestContext(request))
@login_required
def delete_pool(request,pk):
    pool = Pool.objects.get(pk=pk)
    pool.delete()
    return redirect('pools') 
@login_required
def delete_sample(request,pk):
    sample = Sample.objects.get(pk=pk)
    sample.delete()
    return redirect('samples')
@login_required
def delete_project(request,pk):
    project = Project.objects.get(pk=pk)
    project.delete()
    return redirect('projects')


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
    workflow_form = AngularFormDecorator(WorkflowForm)(instance=workflow,prefix="workflow")
#     if request.POST.get('workflow',False):
#         workflow_form = WorkflowForm(request.POST,instance=workflow)
#         if workflow_form.is_valid():
#             workflow_form.save()
#     else:
#         workflow_form = WorkflowForm(instance=workflow)
    processes = []
    
    for process in workflow.processes.all():
#         print "%s:%s"%(request.POST.get('process_id'),process.id)
#         if request.POST and request.POST.get('process_id','') == str(process.id):
#             print "POST!!!!(%s)" %  str(process.id)
#             form = ProcessForm(request.POST,instance=process)
#             form.is_valid()
#             print form.cleaned_data
#             if form.is_valid():
#                 form.save(commit=True)
#                 print 'SAVING!!'
#             processes.append({'process':process, 'form':form, 'valid':form.is_valid(),'submitted':True})
#         else:
        processes.append({'process':process, 'form':AngularFormDecorator(ProcessForm)(instance=process,prefix="process_%d"%process.id)})
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
            