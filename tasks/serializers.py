from rest_framework import serializers
from models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(many=False,read_only=True)
    modified_by = serializers.StringRelatedField(many=False,read_only=True)
    class Meta:
        model = Task
        fields = '__all__'
