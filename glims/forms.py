from django import forms
from glims.models import Lab, Sample
from extensible.models import ModelType
from extensible.forms import ExtensibleModelForm
from autocomplete_light.widgets import ChoiceWidget

class FullSampleForm(ExtensibleModelForm):
    class Meta:
        model = Sample
        exclude = ('data','sample_id','type')
        autocomplete_fields = ("project")
#         widgets = {
#            "project":ChoiceWidget("ProjectAutocomplete"),
#         }

class LabForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = ('name','affiliation','url','description','slug')

class UploadFileForm(forms.Form):
    subdir = forms.CharField(max_length=200)
    filename = forms.CharField(max_length=200)
    overwrite = forms.BooleanField(required=False)
    file = forms.FileField()
