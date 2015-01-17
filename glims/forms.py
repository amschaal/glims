from django import forms
from glims.lims import Project, Sample, ModelType, WorkflowTemplate, Workflow, Process, Pool
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div, HTML

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
    if not field.has_key('kwargs'):
        field['kwargs']={}
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
#         try:
#             kwargs['initial'] = float(kwargs['initial'])
#         except Exception:
#             pass
        return forms.FloatField(**kwargs)
    if field['class'] == 'IntegerField':
#         try:
#             kwargs['initial'] = int(kwargs['initial'])
#         except Exception:
#             pass
        return forms.IntegerField(**kwargs)
    if field['class'] == 'BooleanField':
#         kwargs['initial'] = True if kwargs['initial']=='true' else False
        return forms.BooleanField(**kwargs)

class ExtensibleModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        angular_prefix = kwargs.pop('angular_prefix', None)
        field_template = kwargs.pop('field_template', None)
        ajax_only = kwargs.pop('ajax_only', None)
        #Change any AJAX submitted data into same format expected by form data
        if len(args) > 0:
            if args[0].has_key('data'):
                if isinstance(args[0]['data'], dict):
                    for key,value in args[0]['data'].iteritems():
                        args[0]['data__'+key]=value    
        super(ExtensibleModelForm,self).__init__(*args, **kwargs)
        
        
        
        
        content_type = self.__class__._meta.model.__name__.lower()
        instance = kwargs.get('instance', None)
        if self.fields.has_key('type'):
            self.fields['type'].queryset = ModelType.objects.filter(content_type=content_type)
        if instance:
            if instance.type:
#                 print instance.type.schema
#                 print instance.data
                if instance.type.schema:
                    for field in instance.type.schema:
                        field_name = 'data__%s'%field['name']
                        initial = instance.data[field['name']] if instance.data.has_key(field['name']) else None
                        self.fields[field_name] = get_field(field,initial)
        if angular_prefix:
            for field in self.fields.keys():
                print "content_type:%s"% content_type
                kwargs = {'ng-model':'%s.%s'%(angular_prefix,field.replace('data__','data.'))}
                if not ajax_only:
                    kwargs['initial-value']=''
                self.fields[field].widget.attrs.update(kwargs)
                
        if field_template:
            self.helper = FormHelper(self)
            self.helper.field_template = field_template
        
        
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

class PoolForm(ExtensibleModelForm):
    class Meta:
        model = Pool
        exclude = ('data','refs','samples','sample_data')

class WorkflowTemplateForm(forms.ModelForm):
    class Meta:
        model = WorkflowTemplate
    def __init__(self,*args,**kwargs):
        super(forms.ModelForm,self).__init__(*args, **kwargs)
        self.fields['type'].queryset = ModelType.objects.filter(content_type='workflow')

class WorkflowProcessForm(forms.ModelForm):
    class Meta:
        model = WorkflowTemplate
    def __init__(self,*args,**kwargs):
        super(forms.ModelForm,self).__init__(*args, **kwargs)
        self.fields['process'].queryset = ModelType.objects.filter(content_type='process')

class CreateWorkflowForm(forms.ModelForm):
    class Meta:
        model = Workflow
        fields = ('workflow_template','name','description')

class WorkflowForm(ExtensibleModelForm):
    class Meta:
        model = Workflow
        exclude = exclude = ('type','data','refs','workflow_template','samples')
        
class ProcessForm(ExtensibleModelForm):
    class Meta:
        model = Process
        exclude =  ('type','data','refs','workflow','sample_data')

# class ProcessTemplate(models.Model):
#     type = models.ForeignKey(ModelType)
#     name = models.CharField(max_length=100)
#     description = models.TextField(null=True,blank=True)
# 
# class WorkflowTemplate(models.Model):
#     type = models.ForeignKey(ModelType)
#     name = models.CharField(max_length=100)
#     description = models.TextField(null=True,blank=True)
#     process_templates = models.ManyToManyField(ProcessTemplate,through="WorkflowProcess")


