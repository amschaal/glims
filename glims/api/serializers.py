from rest_framework import serializers
from glims.lims import Project, Sample, ModelType, Pool, Lab
from django_compute.models import Job

# from jsonfield import JSONField
from glims.models import StatusOption
from django.contrib.auth.models import User
from rest_framework.fields import DictField
from extensible.drf import DRFFieldHandler
from glims.api.fields import JSONField, ModelRelatedField

class ModelTypeSerializer(serializers.ModelSerializer):
    content_type__model = serializers.CharField(source='content_type.model',read_only=True)
    fields = JSONField()
    class Meta:
        model = ModelType
#         field=('name','description','fields','content_type__model')

#Takes a list of fields, for dynamic nested serializers.  Used by ExtensibleSerializer. 
class DataSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        print "DATA SERIALIZER"
        fields = kwargs.pop('fields',[])
        read_only = kwargs.pop('read_only',False)
#         if self.model_type:
#             serializer_fields = self.get_model_type_fields(self.model_type)
        for key,field in fields.iteritems():
            if read_only:
                field.required = False
            self.fields[key] = field
            
        super(DataSerializer, self).__init__(*args,**kwargs)
        for key, field in self.fields.iteritems():
            if hasattr(field, 'source'):
                field.source = None


class ExtensibleSerializer(serializers.ModelSerializer):
    type = ModelRelatedField(model=ModelType,serializer=ModelTypeSerializer,required=False,allow_null=True)
    type__name = serializers.StringRelatedField(source='type.name',read_only=True)
    data = DictField(default={},required=False)
    def __init__(self, *args, **kwargs):
        self.model_type_fields = {}
        self.model_type = kwargs.pop('model_type',None)
        super(ExtensibleSerializer, self).__init__(*args,**kwargs)
        if self.model_type:
            self.fields['data'] = DataSerializer(fields=self.get_model_type_fields(self.model_type))
        
    def update(self, instance, validated_data):
        self.fields['data'] = DictField() #hacky, figure out how to serialize to nested DataSerializer
        validated_data['data'] = {key:str(value) for key,value in validated_data.get('data',{}).items()} #HStore only takes strings
        return super(ExtensibleSerializer, self).update(instance,validated_data)
    def create(self, validated_data):
        self.fields['data'] = DictField() #hacky, figure out how to serialize to nested DataSerializer
        validated_data['data'] = {key:str(value) for key,value in validated_data.get('data',{}).items()} #HStore only takes strings
        return super(ExtensibleSerializer, self).create(validated_data)
    def to_representation(self, instance ):
        print 'REPRESENT'
        print instance
        rep = super(ExtensibleSerializer, self).to_representation(instance)
        if hasattr(instance, 'type_id'):
            print instance.data
            print self.get_model_type_fields(instance.type_id)
#             print DataSerializer(instance.data,fields=self.get_model_type_fields(instance.type_id)).data
            rep['data'] = DataSerializer(instance.data,fields=self.get_model_type_fields(instance.type_id),read_only=True).data
        return rep
    def get_model_type_fields(self,model_type):
        if not self.model_type_fields.has_key(str(model_type)):
            self.model_type_fields[str(model_type)] = DRFFieldHandler(ModelType.objects.get(id=model_type).fields).get_fields()
        return self.model_type_fields[str(model_type)]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','last_login','first_name','last_name','email','groups')

class StatusOptionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="status.id")
    name = serializers.CharField(source="status.name")
    class Meta:
        model = StatusOption
        fields = ('id','name','order')
         
class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab

class ProjectSerializer(ExtensibleSerializer):
    lab__name = serializers.CharField(source='lab.name',read_only=True)
    sample_type = ModelRelatedField(model=ModelType,serializer=ModelTypeSerializer)
    type__name = serializers.StringRelatedField(source='type.name',read_only=True)
    status_options = StatusOptionSerializer(many=True,read_only=True,source='type.status_options')
    lab = ModelRelatedField(model=Lab,serializer=LabSerializer)
    history = JSONField(read_only=True)
    class Meta:
        model = Project
#         fields = ('id','name','type','type__name','sample_type','description','lab','lab__name','data','created','status','history','status_options')

        
class SampleSerializer(ExtensibleSerializer):
    project__name = serializers.CharField(source='project.name',read_only=True)
    project = ModelRelatedField(model=Project,serializer=ProjectSerializer)
    class Meta:
        model = Sample
        read_only_fields = ('sample_id','project__name','type__name')
#         fields = ('id','sample_id','project_id','name','description','project'lab','lab__name','data')
#         fields = ('id','sample_id','project_id','name','description','project__name')

class PoolSerializer(ExtensibleSerializer):
    type__name = serializers.StringRelatedField(source='type.name',read_only=True)
    sample_data = DictField(default={},required=False)
    class Meta:
        model = Pool

class JobSerializer(serializers.ModelSerializer):
    data = JSONField()
    params = JSONField()
    args = JSONField()
    class Meta:
        model = Job
        fields = ('id','job_id','template','params','created','run_at','args','status','data')


