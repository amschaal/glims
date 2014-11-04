from django.shortcuts import render
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.db.models import Q
from lims import *
from django.contrib.auth.decorators import login_required
from permissions.manage import get_all_user_objects

# @login_required
def home(request):
    return render(request, 'glims/dashboard.html', {},context_instance=RequestContext(request))
def study(request, pk):
    study = Study.objects.get(pk=pk)
    return render(request, 'glims/study.html', {'study':study} ,context_instance=RequestContext(request))
def sample(request,pk):
    sample = Sample.objects.get(pk=pk)
    return render(request, 'glims/sample.html', {'sample':sample} ,context_instance=RequestContext(request))
def experiment(request,pk):
    experiment = Experiment.objects.get(pk=pk)
    return render(request, 'glims/experiment.html', {'experiment':experiment} ,context_instance=RequestContext(request))
def studies(request):
    studies = get_all_user_objects(request.user, ['view'], Study)#Study.objects.all()
    return render(request, 'glims/studies.html', {'studies':studies} ,context_instance=RequestContext(request))
def samples(request):
    samples = get_all_user_objects(request.user, ['view'], Sample)#Sample.objects.all()
    return render(request, 'glims/samples.html', {'samples':samples} ,context_instance=RequestContext(request))
def experiments(request):
    experiments = get_all_user_objects(request.user, ['view'], Experiment)#Experiment.objects.all()
    return render(request, 'glims/experiments.html', {'experiments':experiments} ,context_instance=RequestContext(request))