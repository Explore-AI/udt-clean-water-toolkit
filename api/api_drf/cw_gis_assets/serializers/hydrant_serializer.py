from cwageodjango.assets.models import Hydrant
from rest_framework import serializers
from config.serializers import BaseGeoJsonSerializer

class HydrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hydrant
        fields = ["gid", "geometry", "dmas", "modified_at", "created_at"]

class HydrantGeoJsonSerializer(BaseGeoJsonSerializer):
    class Meta:
        model = Hydrant
        fields = ["geojson"]
        