from django import forms
from glims.lims import Project, Sample, Experiment, ModelType

# class FileForm(ModelForm):
#     class Meta:
#         model = File
#         fields = ['file','name','description']

# class UpdateFileForm(ModelForm):
#     class Meta:
#         model = File
#         fields = ['name','description']
def get_field(field={}, initial=None):
    
    kwargs = {'initial':initial}
    kwargs['label'] = field['kwargs']['label'] if field['kwargs'].has_key('label') else field['name']
    kwargs['required'] = field['kwargs']['required'] if field['kwargs'].has_key('required') else False
    if field.has_key('__meta__'):
        if field['__meta__'].has_key('label'):
            kwargs['label'] = field['__meta__']['label'] 
        if field['__meta__'].has_key('widget'):
            if field['__meta__']['widget'] == 'Select':
                kwargs['widget'] = forms.Select(choices=field['kwargs']['choices'])
            if field['__meta__']['widget'] == 'RadioSelect':
                kwargs['widget'] = forms.RadioSelect(choices=field['kwargs']['choices'])
            if field['__meta__']['widget'] == 'Textarea':
                kwargs['widget'] = forms.Textarea()
    if field['class'] == 'CharField':
        return forms.CharField(**kwargs)
    if field['class'] == 'FloatField':
        try:
            kwargs['initial'] = float(kwargs['initial'])
        except Exception:
            pass
        return forms.FloatField(**kwargs)
    if field['class'] == 'IntegerField':
        try:
            kwargs['initial'] = int(kwargs['initial'])
        except Exception:
            pass
        return forms.IntegerField(**kwargs)
    if field['class'] == 'BooleanField':
        kwargs['initial'] = True if kwargs['initial']=='true' else False
        return forms.BooleanField(**kwargs)

class ExtensibleModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ExtensibleModelForm,self).__init__(*args, **kwargs)
        content_type = self.__class__._meta.model.__name__.lower()
        instance = kwargs.get('instance', None)
        self.fields['type'].queryset = ModelType.objects.filter(content_type=content_type)
        if instance:
            if instance.type:
#                 print instance.type.schema
#                 print instance.data
                for field in instance.type.schema:
                    field_name = 'data__%s'%field['name']
                    initial = instance.data[field['name']] if instance.data.has_key(field['name']) else None
                    self.fields[field_name] = get_field(field,initial)
    def save(self, commit=True):
        instance = super(ExtensibleModelForm, self).save(commit=False)
        for key in self.cleaned_data.keys():
            if key[:6] == 'data__':
                instance.data[key[6:]] = self.cleaned_data[key]
        if commit:
            instance.save()
        return instance


class ProjectForm(ExtensibleModelForm):
    class Meta:
        model = Project
        exclude = ('data','refs')

class SampleForm(ExtensibleModelForm):
    class Meta:
        model = Sample
        exclude = ('data','refs')

class ExperimentForm(ExtensibleModelForm):
    class Meta:
        model = Experiment
        exclude = ('data','refs')
