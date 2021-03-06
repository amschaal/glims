from django.shortcuts import render, redirect, get_object_or_404
from django.template.context import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from glims.models import *
from django.contrib.auth.decorators import login_required
from sendfile import sendfile
from forms import LabForm
import json 
from django_compute.models import Job

@login_required
def home(request):
    return render(request, 'glims/home.html', {})
@login_required
def project(request, pk):
    project = Project.objects.get(pk=pk)
    content_type_id = ContentType.objects.get_for_model(project).id
    return render(request, 'glims/project.html', {'project':project,'content_type_id':content_type_id} )
@login_required
def sample(request,pk):
    sample = Sample.objects.get(pk=pk)
    return render(request, 'glims/sample.html', {'sample':sample} )
@login_required
def pool(request,pk):
    pool = Pool.objects.get(pk=pk)
#     samples = SampleSerializer(pool.samples.all()).data
#     form = AngularFormDecorator(PoolForm)(instance=pool,prefix="pool")
#     sample_form = AngularFormDecorator(PoolForm)(instance=pool,prefix="sample",field_template='glims/crispy/sample_field.html')
    return render(request, 'glims/pool.html', {'pool':pool} )
@login_required
def labs(request):
    return render(request, 'glims/labs.html', {} )
@login_required
def lab(request, pk):
    lab = Lab.objects.get(pk=pk)
#     inlines = ModelTypePlugins.objects.filter(type=project.type,layout=ModelTypePlugins.INLINE_LAYOUT, plugin__page='project').order_by('weight')
#     tabs = ModelTypePlugins.objects.filter(type=project.type,layout=ModelTypePlugins.TABBED_LAYOUT, plugin__page='project').order_by('weight')
    return render(request, 'glims/lab.html', {'lab':lab} )
@login_required
def projects(request):
#     projects = get_all_user_objects(request.user, ['view'], Project)#Project.objects.all()
    query = json.dumps(request.GET)
    content_type_id = ContentType.objects.get_for_model(Project).id
    return render(request, 'glims/projects.html', {'query':query,'content_type_id':content_type_id} )
@login_required
def samples(request):
    query = json.dumps(request.GET)
#     samples = get_all_user_objects(request.user, ['view'], Sample)#Sample.objects.all()
    return render(request, 'glims/samples.html', {'query':query} )
@login_required
def pools(request):
    return render(request, 'glims/pools.html', {} )
@login_required
def jobs(request):
    return render(request, 'glims/jobs.html', {} )
@login_required
def job(request,id):
    job = Job.objects.get(id=id)
    return render(request, 'glims/job.html', {'job':job} )
@login_required
def job_files(request,id):
    job = Job.objects.get(id=id)
    return render(request, 'glims/job_files.html', {'job':job} )
@login_required
def cart(request):
    return render(request, 'glims/cart.html', {} )
@login_required
def model_types(request):
    content_types = ContentType.objects.all()
    return render(request, 'glims/model_types.html', {'content_types':content_types} )
@login_required
def model_type(request,pk):
    model_type = ModelType.objects.get(pk=pk)
    init = {'fields':model_type.fields,'name':model_type.name,'description':model_type.description,'content_type':model_type.content_type.id,'id':model_type.id,'urls':{'update':reverse('update_model_type',kwargs={"pk":pk})}}#{'update':reverse('update_model_type',kwargs={"pk":pk})}
    return render(request, 'glims/model_type.html', {'init':json.dumps(init),'model_type':model_type})
#     return render(request, 'glims/model_type.html', {'job':job} )

@login_required
def create_lab(request):
    if request.method == 'GET':
        form = LabForm()
    elif request.method == 'POST':
        form = LabForm(request.POST)
        if form.is_valid():
            lab = form.save()
            return redirect(reverse('lab',kwargs={'pk':lab.pk})) 
    return render(request, 'glims/create_lab.html', {'form':form} )

@login_required
def modify_lab(request,pk):
    lab = get_object_or_404(Lab,pk=pk)
    if request.method == 'GET':
        form = LabForm(instance=lab)
    elif request.method == 'POST':
        form = LabForm(request.POST,instance=lab)
        if form.is_valid():
            lab = form.save()
            return redirect(reverse('lab',kwargs={'pk':lab.pk})) 
    return render(request, 'glims/modify_lab.html', {'form':form,'lab':lab} )

@login_required
def choose_project_type(request):
    form = ProjectTypeForm(initial={'lab':request.GET.get('lab',None)})
    return render(request, 'glims/choose_project_type.html', {'form':form} )

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

