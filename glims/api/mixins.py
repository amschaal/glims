import os

from glims.forms import UploadFileForm
from glims.settings import FILES_ROOT
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route
from django.utils._os import safe_join
from sendfile import sendfile
from datetime import datetime

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
        
#             file={'name':name,'extension':name.split('.').pop() if '.' in name else None,'size':sizeof_fmt(size),'bytes':size,'modified':datetime.datetime.fromtimestamp(mtime).strftime("%m/%d/%Y %I:%M %p"),'metadata':metadata,'isText':istext(path)}
        list = []
        for name in os.listdir(path):
            full_path = os.path.join(path,name)
            if os.path.isdir(full_path):
                list.append({'name':name,'is_dir':True})
            else:
                extension = os.path.splitext(full_path)[1]
                if len(self.extension_filters) == 0 or extension in self.extension_filters:
                    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(full_path)
                    list.append({'name':name,'is_dir':False,'extension':extension,'bytes':size,'modified':datetime.fromtimestamp(mtime).strftime("%m/%d/%Y %I:%M %p")})
        return Response({"basedir":self.get_directory(),"subdir":subdir,"files":list})

class FileMixin(FileMixinBase):
    def handle_uploaded_file(self,f,path,filename=None):
        if not os.path.exists(path):
            os.makedirs(path)
        filename = filename or f.name
        upload_to = safe_join(path,filename)
        with open(upload_to, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    #curl -X POST -H "Content-Type:multipart/form-data" -H 'Authorization: Token 12345' -F "file=@{filename};" -F "subdir=subdir_name" http://localhost/api/resource/:id/upload_file/
    @detail_route(methods=['post'])
    def upload_file(self, request, pk=None):
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            path = os.path.join(self.get_directory(),'files',form.cleaned_data['subdir'])
            file = request.FILES['file']
            filename = form.cleaned_data['filename'] or file.name
            if not form.cleaned_data['overwrite'] and os.path.exists(safe_join(path,filename)):
                return Response({'file':['File "%s" exists at path "%s"'%(filename,path)]}, status=status.HTTP_400_BAD_REQUEST)
            self.handle_uploaded_file(file,path,filename)
            return Response({'status': 'success'})
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class FileDownloadMixin(FileMixinBase):
    @detail_route(methods=['get'])
    def download(self, request, pk=None):
        subpath = request.query_params.get('subpath')
        path = safe_join(self.get_directory(),subpath)
        return sendfile(request, path, attachment=True)

class FileManagerMixin(FileDownloadMixin,FileMixin,FileBrowserMixin):
    pass
