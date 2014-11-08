from django.forms import ModelForm
from glims.lims import File, Study, Sample, Experiment

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['file','name','description']

class UpdateFileForm(ModelForm):
    class Meta:
        model = File
        fields = ['name','description']
        
class StudyForm(ModelForm):
    class Meta:
        model = Study

class SampleForm(ModelForm):
    class Meta:
        model = Sample

class ExperimentForm(ModelForm):
    class Meta:
        model = Experiment
