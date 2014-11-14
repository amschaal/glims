from django.forms import ModelForm
from glims.lims import Project, Sample, Experiment#, File

# class FileForm(ModelForm):
#     class Meta:
#         model = File
#         fields = ['file','name','description']

# class UpdateFileForm(ModelForm):
#     class Meta:
#         model = File
#         fields = ['name','description']
        
class ProjectForm(ModelForm):
    class Meta:
        model = Project

class SampleForm(ModelForm):
    class Meta:
        model = Sample

class ExperimentForm(ModelForm):
    class Meta:
        model = Experiment
