from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
import json
from tracker.models import Log, Export
from glims.models import Project
import csv

@login_required
def exports(request):
    return render(request, 'tracker/exports.html', {'statuses':json.dumps(dict(Log.STATUS_CHOICES))} ,context_instance=RequestContext(request))

@login_required
def project_report(request):
    export_id = request.GET.get('export_id')
    log_ids = request.GET.getlist('log_ids',None)
    if export_id:
        log_ids = Export.objects.get(id=export_id).logs.values_list('id')
    print export_id
    print log_ids
    projects = Project.objects.filter(tracker_logs__id__in=log_ids).distinct().prefetch_related('tracker_logs')
    print projects
    response = HttpResponse(content_type='text/tsv')
    response['Content-Disposition'] = 'attachment; filename="log_project_report.tsv"'

    writer = csv.writer(response,dialect=csv.excel_tab)
    writer.writerow(['Project','Lab','Count','Total','Users','Start date','End date'])
    for p in projects:
        logs = p.tracker_logs.filter(id__in=log_ids)
        total = sum(l.quantity for l in logs)
        users = ",".join(set(l.user.name for l in logs))
        writer.writerow([p.name, p.lab.name,logs.count(),total,users,logs.order_by('created').first().created,logs.order_by('-created').first().created])

    return response
    
    
        
