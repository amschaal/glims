from plugins.models import Plugin, ModelTypePlugin
from rest_framework import serializers
from extensible.drf.fields import ModelRelatedField


class PluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plugin
#         fields = ('id','name')

class ModelTypePluginSerializer(serializers.ModelSerializer):
#     model
#     plugin_details = 
    plugin = ModelRelatedField(model=Plugin,serializer=PluginSerializer)
    class Meta:
        model = ModelTypePlugin
