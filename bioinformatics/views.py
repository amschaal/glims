from django.shortcuts import render
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required


@login_required
def bioinfo_projects(request):
    return render(request, 'bioinformatics/bioinfo_projects.html', {} ,context_instance=RequestContext(request))
