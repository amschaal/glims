from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
import json
from tracker.models import Log

@login_required
def exports(request):
    return render(request, 'tracker/exports.html', {'statuses':json.dumps(dict(Log.STATUS_CHOICES))} ,context_instance=RequestContext(request))
