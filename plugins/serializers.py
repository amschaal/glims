from plugins.models import Plugin, ModelTypePlugin
from rest_framework import serializers
from extensible.drf.fields import ModelRelatedField


class PluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plugin
        fields = '__all__'

class ModelTypePluginSerializer(serializers.ModelSerializer):
    plugin = ModelRelatedField(model=Plugin,serializer=PluginSerializer)
    class Meta:
        model = ModelTypePlugin
        fields = '__all__'
