from rest_framework import serializers
from sequencing.models import Machine, Lane, Run
from glims.api.fields import ModelRelatedField
from glims.models import Pool
from glims.api.serializers import FlatPoolSerializer

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine

class LaneSerializer(serializers.ModelSerializer):
    pool = ModelRelatedField(model=Pool,serializer=FlatPoolSerializer)
    class Meta:
        model = Lane

class RunSerializer(serializers.ModelSerializer):
    machine = ModelRelatedField(model=Machine,serializer=MachineSerializer)
    lanes = LaneSerializer(many=True,read_only=True)
    class Meta:
        model = Run