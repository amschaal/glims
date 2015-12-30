from bioinformatics.models import BioinfoProject
from django import forms
class BioinfoProjectForm(forms.ModelForm):
    class Meta:
        model = BioinfoProject
        fields = ('assigned_to','description',)
