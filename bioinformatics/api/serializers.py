from rest_framework import serializers
from bioinformatics.models import BioinfoProject
from glims.api.serializers import ProjectSerializer, ModelRelatedField, UserSerializer
from django.contrib.auth.models import User


class BioinfoProjectSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True,many=False)
    manager = ModelRelatedField(model=User,serializer=UserSerializer,queryset=User.objects.filter(groups__id=1))
    participants = ModelRelatedField(model=User,serializer=UserSerializer,many=True,queryset=User.objects.filter(groups__id=1))
#     participants = ManyUserField(queryset=User.objects.all())
    class Meta:
        model = BioinfoProject
        fields = ('id','name','project','created','manager','participants','description')
