from rest_framework import serializers
from models import Log, Category
from rest_framework.fields import CurrentUserDefault
from django.contrib.auth.models import User
from glims.api.serializers import UserSerializer
from glims.api.fields import ModelRelatedField

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
class LogSerializer(serializers.ModelSerializer):
    user = ModelRelatedField(model=User,serializer=UserSerializer,default=CurrentUserDefault())#serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),default=CurrentUserDefault())
    category = ModelRelatedField(model=Category,serializer=CategorySerializer)
    class Meta:
        model = Log
        

