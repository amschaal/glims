from bioinformatics.models import BioinfoProject
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
class BioinfoProjectForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (BioinfoProjectForm,self).__init__(*args,**kwargs) # populates the post
        self.fields['assigned_to'].queryset = User.objects.filter(groups__id=settings.BIOCORE_ID)
    class Meta:
        model = BioinfoProject
        fields = ('assigned_to','description',)
