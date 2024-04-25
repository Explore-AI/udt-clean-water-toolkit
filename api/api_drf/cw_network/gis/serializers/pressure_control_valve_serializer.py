from cwa_geod.assets.models import PressureControlValve
from rest_framework import serializers 

class PressureControlValveSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = PressureControlValve
        fields = ['gid', 'geometry', 'dmas', 'modified_at', 'created_at']