from django import forms
from django.contrib.auth.models import User, Group
class PermissionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        model = kwargs.pop('model')
        super(PermissionForm, self).__init__(*args, **kwargs)
        self.fields["permissions"] = forms.MultipleChoiceField(label='Permissions', required=False, 
                    widget=forms.CheckboxSelectMultiple, choices = model._meta.permissions)
#     user = forms.IntegerField()
#     user = forms.ModelChoiceField(queryset=User.objects.all())
#     permission
class UserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    
class GroupForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all())