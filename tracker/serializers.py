from rest_framework import serializers
from models import Log, Category, Export
from rest_framework.fields import CurrentUserDefault
from django.contrib.auth.models import User
from glims.api.serializers import UserSerializer
from glims.api.fields import ModelRelatedField
from glims.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    lab = serializers.CharField(source='lab.name',read_only=True)
    class Meta:
        model = Project
        fields = ('id','name','lab')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ExportSerializer(serializers.ModelSerializer):
    created_by = ModelRelatedField(model=User,serializer=UserSerializer,default=CurrentUserDefault())#serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),default=CurrentUserDefault())
#     logs = ExportLogSerializer(read_only=True, many=True)#ModelRelatedField(model=Log,serializer=ExportLogSerializer,many=True,allow_empty=True)
    start_date = serializers.DateTimeField()#serializers.SerializerMethodField()
    end_date = serializers.DateTimeField()
    class Meta:
        model = Export
        fields = '__all__'
        read_only_fields = ('logs',)

class LogExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Export
        exclude = ('logs',)

class LogSerializer(serializers.ModelSerializer):
    user = ModelRelatedField(model=User,serializer=UserSerializer,default=CurrentUserDefault())#serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),default=CurrentUserDefault())
    category = ModelRelatedField(model=Category,serializer=CategorySerializer)
    project = ModelRelatedField(model=Project,serializer=ProjectSerializer)
    exports = LogExportSerializer(many=True,read_only=True)
    class Meta:
        model = Log
        fields = '__all__'
