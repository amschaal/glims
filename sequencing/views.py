from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext

@login_required
def runs(request):
    return render(request, 'sequencing/runs.html', {} ,context_instance=RequestContext(request))