from django.forms import ModelForm
from glims.lims import File

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['file','name','description']

class UpdateFileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name','description']