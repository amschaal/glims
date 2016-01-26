from rest_framework import serializers
from glims.lims import Project, Sample, ModelType, Pool, Lab#, File, Note
# from glims.jobs import Job, JobSubmission
from django_compute.models import Job

from jsonfield import JSONField
from glims.models import Status, StatusOption
from django.contrib.auth.models import User
# from rest_framework.fields import WritableField

class ModelRelatedField(serializers.RelatedField):
    model = None
    pk = 'id'
    serializer = None
    def to_internal_value(self, data):
        if isinstance(data, int):
            kwargs = {self.pk:data}
            return self.model.objects.get(**kwargs)
        if data.get(self.pk,None):
            return self.model.objects.get(id=data['id'])
        return None
    def to_representation(self, value):
        return self.serializer(value).data
    def __init__(self, **kwargs):
        self.model = kwargs.pop('model', self.model)
        self.pk = kwargs.pop('pk', self.pk)
        self.serializer = kwargs.pop('serializer', self.serializer)
        assert self.model is not None, (
            'Must set model for ModelRelatedField'
        )
        assert self.serializer is not None, (
            'Must set serializer for ModelRelatedField'
        )
        self.queryset = kwargs.pop('queryset', self.model.objects.all())
        super(ModelRelatedField, self).__init__(**kwargs)

class JSONWritableField(serializers.Field):
    """
    DRF JSON Field
    """
#     def from_native(self, value):
#         import json
#         print value.replace(':','$')
#         if value:
#             return json.dumps(value)#JSONField(value)
#         else:
#             return None
# 
    def to_internal_value(self,value):
        import json
        if not isinstance(value, str) or value is None:
            return value
        value = json.loads(value)#JSONField(value)
        return value
    def to_representation(self, value):
        return value
        import json
        return json.dumps(value)
class JSONField(serializers.Field):
    def to_internal_value(self,value):
        import json
        if not isinstance(value, str) or value is None:
            return value
        value = json.loads(value)#JSONField(value)
        return value
    def to_representation(self, value):
        return value
        import json
        return json.dumps(value)
#     def to_native(self, value):
#         import json
#         if not isinstance(value, str) or value is None:
#             return value
#         value = json.loads(value)#JSONField(value)
#         return value

# class StatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectStatus
#         fields = ('status','set_by','timestamp')

class UserSerializer(serializers.ModelSerializer):
#     type = serializers.StringRelatedField(many=False,read_only=True)
#     type__name = serializers.StringRelatedField(source='type.name')
#     data = JSONWritableField()
#     sample_data = JSONWritableField()
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

class ProjectSerializer(serializers.ModelSerializer):
    lab__name = serializers.CharField(source='lab.name',read_only=True)
#     type = serializers.StringRelatedField(many=False,read_only=True)
    type__name = serializers.StringRelatedField(source='type.name',read_only=True)
    status_options = StatusOptionSerializer(many=True,read_only=True,source='type.status_options')
    lab = ModelRelatedField(model=Lab,serializer=LabSerializer)
    data = JSONWritableField()
    history = JSONWritableField(read_only=True)
#     history = JSONWritableField()
#     def __init__(self,*args,**kwargs):
#         super(ProjectSerializer,self).__init__(*args,**kwargs)
#         print self.instance.type.status_options
    class Meta:
        model = Project
        fields = ('id','name','type','type__name','sample_type','description','lab','lab__name','data','created','status','history','status_options')
#         depth = 4
#         read_only_fields = ('',)

class SampleSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer(many=False,read_only=True)
#     project_id = serializers.RelatedField(many=False)
#     type = serializers.RelatedField(many=False)
    type__name = serializers.StringRelatedField(source='type.name')
    project__name = serializers.CharField(source='project.name')
    data = JSONWritableField()
    class Meta:
        model = Sample
#         fields = ('id','sample_id','project_id','name','description','project'lab','lab__name','data')
#         fields = ('id','sample_id','project_id','name','description','project__name')

class PoolSerializer(serializers.ModelSerializer):
#     project = ProjectSerializer(many=False,read_only=True)
#     project_id = serializers.RelatedField(many=False)
    type = serializers.StringRelatedField(many=False,read_only=True)
    type__name = serializers.StringRelatedField(source='type.name')
    data = JSONWritableField()
    sample_data = JSONWritableField()
    class Meta:
        model = Pool

# class JobSubmissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = JobSubmission

# class JobSerializer(serializers.ModelSerializer):
#     config = JSONWritableField()
#     args = JSONWritableField()
#     class Meta:
#         model = Job
        

class ModelTypeSerializer(serializers.ModelSerializer):
    content_type__model = serializers.CharField(source='content_type.model')
    fields = JSONField()
    class Meta:
        model = ModelType
        field=('name','description','fields','content_type__model')
        
# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         
# class NoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Note
        

        
class JobSerializer(serializers.ModelSerializer):
    data = JSONWritableField()
    params = JSONWritableField()
    args = JSONWritableField()
#     urls = serializers.SerializerMethodField()
#     def get_urls(self,obj):
#         return {'update'}
    class Meta:
        model = Job
        fields = ('id','job_id','template','params','created','run_at','args','status','data')




# class UserField(ModelRelatedField):
#     model = User
#     serializer = UserSerializer
# class LabField(ModelRelatedField):
#     model = Lab
#     serializer = LabSerializer
    
# class UserFieldOld(serializers.RelatedField):
#     def to_internal_value(self, data):
#         if isinstance(data, int):
#             return User.objects.get(id=data)
#         if data.get('id',None):
#             return User.objects.get(id=data['id'])
#         return None
#     def to_representation(self, value):
# #         raise Exception('hello')
#         return UserSerializer(value).data
    
    
# class ManyUserField(serializers.ManyRelatedField):   
#     def to_representation(self, iterable):
#         return ['foo']
#         return [
#             self.child_relation.to_representation(value)
#             for value in iterable
#         ]
