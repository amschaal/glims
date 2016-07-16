import os

from glims.forms import UploadFileForm
from glims.settings import FILES_ROOT
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route
from django.utils._os import safe_join

class FileMixinBase(object):
    directory = None
    def get_directory(self):
        if self.directory:
            return self.directory
        obj = self.get_object()
        if hasattr(obj, 'directory'):
            return safe_join(FILES_ROOT,obj.directory)
        raise Exception('No base directory was specified for "%s"'%str(obj))

class FileBrowserMixin(FileMixinBase):
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAdminUser,)
    extension_filters = []
    ignore = []
    @detail_route(methods=['get'])
    def list_files(self, request, pk=None):
        subdir = request.query_params.get('subdir','')
        path = safe_join(self.get_directory(),subdir)
        list = []
        for name in os.listdir(path):
            full_path = os.path.join(path,name)
            if os.path.isdir(full_path):
                list.append({'name':name,'is_dir':True})
            else:
                extension = os.path.splitext(full_path)[1]
                print extension
                if len(self.extension_filters) > 0:
                    if extension in self.extension_filters:
                        list.append({'name':name,'is_dir':False,'extension':extension})
                else:
                    list.append({'name':name,'is_dir':False,'extension':extension})
        return Response(list)

class FileMixin(FileMixinBase):
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
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            path = os.path.join(self.get_directory(),'files',form.cleaned_data['subdir'])
            self.handle_uploaded_file(request.FILES['file'],path)
            return Response({'status': 'success'})
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
