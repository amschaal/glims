from rest_framework import serializers
from bioinformatics.models import BioinfoProject
from glims.api.serializers import ProjectSerializer, ModelRelatedField, UserSerializer,\
    ExtensibleSerializer, LabSerializer
from django.contrib.auth.models import User
from glims.lims import Lab, Project


class BioinfoProjectSerializer(ExtensibleSerializer):
#     project = ProjectSerializer(read_only=True,many=False)
    project = ModelRelatedField(model=Project,serializer=ProjectSerializer,required=False,allow_null=True)
    lab = ModelRelatedField(model=Lab,serializer=LabSerializer)
    manager = ModelRelatedField(model=User,serializer=UserSerializer,queryset=User.objects.filter(groups__id=1))
    participants = ModelRelatedField(model=User,serializer=UserSerializer,many=True,queryset=User.objects.filter(groups__id=1),required=False,allow_null=True)
#     participants = ManyUserField(queryset=User.objects.all())
    class Meta:
        model = BioinfoProject
#         fields = ('id','type','name','project','lab','created','manager','participants','description','data_location','data')
