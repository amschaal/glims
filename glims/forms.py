from django import forms
from glims.lims import Project, Sample, WorkflowTemplate, Workflow, Process, Pool,\
    Lab
from extensible.models import ModelType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div, HTML
import json
from extensible.forms import ExtensibleModelForm
from angular_forms.forms.widgets import AngularSelectWidget
import autocomplete_light
# class FileForm(ModelForm):
#     class Meta:
#         model = File
#         fields = ['file','name','description']

# class UpdateFileForm(ModelForm):
#     class Meta:
#         model = File
#         fields = ['name','description']

# @deprecated
# def get_field(field={}, initial=None):
#     
#     kwargs = {'initial':initial}
#     if not field.has_key('kwargs'):
#         field['kwargs']={}
#     kwargs['label'] = field['kwargs']['label'] if field['kwargs'].has_key('label') else field['name']
#     kwargs['required'] = field['kwargs']['required'] if field['kwargs'].has_key('required') else False
#     if field.has_key('__meta__'):
#         if field['__meta__'].has_key('label'):
#             kwargs['label'] = field['__meta__']['label'] 
#         if field['__meta__'].has_key('widget'):
#             if field['__meta__']['widget'] == 'Select':
#                 kwargs['widget'] = forms.Select(choices=field['kwargs']['choices'])
#             if field['__meta__']['widget'] == 'RadioSelect':
#                 kwargs['widget'] = forms.RadioSelect(choices=field['kwargs']['choices'])
#             if field['__meta__']['widget'] == 'Textarea':
#                 kwargs['widget'] = forms.Textarea()
#     if field['class'] == 'CharField':
#         return forms.CharField(**kwargs)
#     if field['class'] == 'FloatField':
# #         try:
# #             kwargs['initial'] = float(kwargs['initial'])
# #         except Exception:
# #             pass
#         return forms.FloatField(**kwargs)
#     if field['class'] == 'IntegerField':
# #         try:
# #             kwargs['initial'] = int(kwargs['initial'])
# #         except Exception:
# #             pass
#         return forms.IntegerField(**kwargs)
#     if field['class'] == 'BooleanField':
# #         kwargs['initial'] = True if kwargs['initial']=='true' else False
#         return forms.BooleanField(**kwargs)
# 
# 
# 
# class JSONForm(forms.Form):
#     def __init__(self,*args,**kwargs):
#         try:
#             fields = json.loads(kwargs.pop('fields','[]'))
#         except:
#             fields = kwargs.pop('fields',[])
#         super(JSONForm, self).__init__(*args, **kwargs)
#         fh = FieldHandler(fields)
#         self.fields = fh.formfields
#         
# 
# class FieldHandler():
#     def __init__(self, fields, initial={}):
#         self.formfields = {}
#         self.initial = initial
#         for field in fields:
#             options = self.get_options(field)
#             f = getattr(self, "create_field_for_"+field['type'] )(field, options)
#             self.formfields[field['name']] = f
# 
#     def get_options(self, field):
#         options = {}
#         options['label'] = field['label']
#         options['help_text'] = field.get("help_text", None)
#         options['required'] = bool(field.get("required", 0) )
#         if self.initial.has_key(field['name']):
#             options['initial']=self.initial[field['name']]
#         return options
# 
#     def create_field_for_text(self, field, options):
#         options['max_length'] = int(field.get("max_length", "20") )
#         return forms.CharField(**options)
#     
#     def create_field_for_file(self, field, options):
#         return forms.FileField(**options)
#     
#     def create_field_for_textarea(self, field, options):
#         options['max_length'] = int(field.get("max_value", "9999") )
#         return forms.CharField(widget=forms.Textarea, **options)
# 
#     def create_field_for_integer(self, field, options):
#         options['max_value'] = int(field.get("max_value", "999999999") )
#         options['min_value'] = int(field.get("min_value", "-999999999") )
#         return forms.IntegerField(**options)
# 
#     def create_field_for_radio(self, field, options):
#         options['choices'] = [ (c['value'], c['name'] ) for c in field['choices'] ]
#         return forms.ChoiceField(widget=forms.RadioSelect,   **options)
# 
#     def create_field_for_select(self, field, options):
#         options['choices']  = [ (c['value'], c['name'] ) for c in field['choices'] ]
#         return forms.ChoiceField(  **options)
# 
#     def create_field_for_checkbox(self, field, options):
#         return forms.BooleanField(widget=forms.CheckboxInput, **options)
# 
# 
# 
# 
# 
# class ExtensibleModelForm(forms.ModelForm):
#     def __init__(self,*args,**kwargs):
#         angular_prefix = kwargs.pop('angular_prefix', None)
#         field_template = kwargs.pop('field_template', None)
#         ajax_only = kwargs.pop('ajax_only', None)
#         #Change any AJAX submitted data into same format expected by form data
#         if len(args) > 0:
#             if args[0].has_key('data'):
#                 if isinstance(args[0]['data'], dict):
#                     for key,value in args[0]['data'].iteritems():
#                         args[0]['data.'+key]=value    
#         super(ExtensibleModelForm,self).__init__(*args, **kwargs)
#         
#         
#         
#         
#         content_type = self.__class__._meta.model.__name__.lower()
#         instance = kwargs.get('instance', None)
#         if self.fields.has_key('type'):
#             self.fields['type'].queryset = ModelType.objects.filter(content_type=content_type)
#         
#         if instance:
#             
#             if instance.type:
# #                 print instance.type.schema
# #                 print instance.data
#                 print 'WTF'
#                 if instance.type.schema:
#                     fh = FieldHandler(instance.type.schema,instance.data)
#                     print "SCHEMA!!"
#                     print instance.type.schema
# #                     jsonform = JSONForm(instance.data,fields=instance.type.schema)
#                     for key, field in fh.formfields.iteritems():
#                         print key
#                         print field
#                         field_name = 'data.%s'%key
# #                         initial = instance.data[field['name']] if instance.data.has_key(field['name']) else None
#                         self.fields[field_name] = field#get_field(field,initial)
# #                     for field in instance.type.schema:
# #                         field_name = 'data.%s'%field['name']
# #                         initial = instance.data[field['name']] if instance.data.has_key(field['name']) else None
# #                         self.fields[field_name] = get_field(field,initial)
#         if angular_prefix:
#             for field in self.fields.keys():
#                 kwargs = {'ng-model': '%s.%s'%(angular_prefix,field)}
#                 if not ajax_only:
#                     kwargs['initial-value']=''
#                 self.fields[field].widget.attrs.update(kwargs)
#                 
#         if field_template:
#             self.helper = FormHelper(self)
#             self.helper.field_template = field_template
# #         for field in self.fields.keys():
# #             ng_model = '%s.%s'%(angular_prefix,field.replace('data__','data.'))
# #             self.fields[field].ng_model = ng_model
#     def save(self, commit=True):
#         instance = super(ExtensibleModelForm, self).save(commit=False)
#         print self.cleaned_data.keys()
#         for key in self.cleaned_data.keys():
#             if key[:5] == 'data.':
#                 instance.data[key[5:]] = self.cleaned_data[key]
#         if commit:
#             instance.save()
#         return instance

class ProjectForm(ExtensibleModelForm):
    samples = forms.ModelMultipleChoiceField(Sample.objects.all(),required=False, widget=autocomplete_light.MultipleChoiceWidget("SampleAutocomplete"))
    class Meta:
        model = Project
#         exclude = ('data','refs')
        fields = ('type','lab','name','description','samples',)
        autocomplete_fields = ("samples")
        widgets = {
           "lab":autocomplete_light.ChoiceWidget("LabAutocomplete"),
        }
#         widgets = {
#            "samples":autocomplete_light.MultipleChoiceWidget("SampleAutocomplete"),
#         }
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.initial['samples'] = [s.pk for s in self.instance.samples.all()]
    def save(self, *args, **kwargs):
        print self.cleaned_data.get('samples')
        for sample in self.cleaned_data.get('samples'):
            sample.project = self.instance
            sample.save()
        return super(ProjectForm, self).save(*args, **kwargs)

class SampleForm(ExtensibleModelForm):
    class Meta:
        model = Sample
        exclude = ('data','refs')
        autocomplete_fields = ("project")
        widgets = {
           "project":autocomplete_light.ChoiceWidget("ProjectAutocomplete"),
        }
#     def __init__(self,*args,**kwargs):
#         super(forms.ModelForm,self).__init__(*args, **kwargs)
#         self.fields['project'].widget = AngularSelectWidget(attrs={'field':'name'})

class PoolForm(ExtensibleModelForm):
    class Meta:
        model = Pool
        exclude = ('data','refs','samples','sample_data')

class WorkflowTemplateForm(forms.ModelForm):
    class Meta:
        model = WorkflowTemplate
    def __init__(self,*args,**kwargs):
        super(forms.ModelForm,self).__init__(*args, **kwargs)
        self.fields['type'].queryset = ModelType.objects.filter(content_type__model='workflow')

class WorkflowProcessForm(forms.ModelForm):
    class Meta:
        model = WorkflowTemplate
    def __init__(self,*args,**kwargs):
        super(forms.ModelForm,self).__init__(*args, **kwargs)
        self.fields['process'].queryset = ModelType.objects.filter(content_type__model='process')

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
        
class LabForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = ('name','description')

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


