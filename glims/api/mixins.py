import os

from glims.forms import UploadFileForm
from glims.settings import FILES_ROOT
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route



class FileMixin(object):
    def handle_uploaded_file(self,f,path):
        if not os.path.exists(path):
            os.makedirs(path)
        upload_to = os.path.join(path,f.name)
        with open(upload_to, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    #curl -X POST -H "Content-Type:multipart/form-data" -H 'Authorization: Token 12345' -F "file=@{filename};" -F "subdir=subdir_name" http://localhost/api/resource/:id/upload_file/
    @detail_route(methods=['post'])
    def upload_file(self, request, pk=None):
        obj = self.get_object()
        if not hasattr(obj, 'directory'):
            raise Exception('%s does not have a directory property'%str(obj))
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            path = os.path.join(FILES_ROOT,obj.directory,'files',form.cleaned_data['subdir'])
            self.handle_uploaded_file(request.FILES['file'],path)
            return Response({'status': 'success'})
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
