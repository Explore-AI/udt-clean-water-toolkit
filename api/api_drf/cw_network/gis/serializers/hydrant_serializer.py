from cwa_geod.assets.models import Hydrant
from rest_framework import serializers 

class HydrantSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Hydrant
        fields = ['gid', 'geometry', 'dmas', 'modified_at', 'created_at']