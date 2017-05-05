from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext

@login_required
def exports(request):
    return render(request, 'tracker/exports.html', {} ,context_instance=RequestContext(request))
