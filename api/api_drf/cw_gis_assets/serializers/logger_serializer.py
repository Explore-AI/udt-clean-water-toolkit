from cwageodjango.assets.models import Logger
from rest_framework import serializers
from config.serializers import BaseGeoJsonSerializer

class LoggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logger
        fields = ["gid", "geometry", "dmas", "modified_at", "created_at"]

class LoggerGeoJsonSerializer(BaseGeoJsonSerializer):
    class Meta:
        model = Logger
        fields = ["geojson"]