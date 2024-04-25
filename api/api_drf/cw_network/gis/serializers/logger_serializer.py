from cwa_geod.assets.models import Logger
from rest_framework import serializers 

class LoggerSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Logger
        fields = ['gid', 'geometry', 'dmas', 'modified_at', 'created_at']