from cwa_geod.assets.models import NetworkMeter
from rest_framework import serializers 

class NetworkMeterSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = NetworkMeter
        fields = ['gid', 'geometry', 'dmas', 'modified_at', 'created_at']