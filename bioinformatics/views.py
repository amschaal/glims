from django.shortcuts import render, get_object_or_404, redirect
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from bioinformatics.models import BioinfoProject
from bioinformatics.forms import BioinfoProjectForm
from django_formly.utils import generate_formly_fields

@login_required
def bioinfo_projects(request):
    return render(request, 'bioinformatics/bioinfo_projects.html', {'group_id':settings.BIOCORE_ID} ,context_instance=RequestContext(request))

@login_required
def bioinfo_project(request,pk):
    instance = get_object_or_404(BioinfoProject,pk=pk)
    formly_fields = generate_formly_fields(BioinfoProjectForm())
    return render(request, 'bioinformatics/bioinfo_project.html', {'instance':instance,'formly_fields':formly_fields} ,context_instance=RequestContext(request))

@login_required
def modify_bioinfo_project(request,pk):
    instance = get_object_or_404(BioinfoProject,pk=pk)
    if request.method == 'POST':
        form = BioinfoProjectForm(request.POST,instance=instance)
        if form.is_valid():
            instance = form.save()
            return redirect('bioinformatics__project',pk=instance.id)
    else:
        form = BioinfoProjectForm(instance=instance)
    return render(request, 'bioinformatics/modify_bioinfo_project.html', {'instance':instance,'form':form} ,context_instance=RequestContext(request))