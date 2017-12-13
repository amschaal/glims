from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from models import Run

@login_required
def runs(request):
    return render(request, 'sequencing/runs.html', {} )
@login_required
def run(request,pk):
    run = Run.objects.get(pk=pk)
    return render(request, 'sequencing/run.html', {'run':run} )