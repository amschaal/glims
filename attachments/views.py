from django.shortcuts import render, redirect
from django.template.context import RequestContext
from models import *
from sendfile import sendfile
from forms import FileForm

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
            
            