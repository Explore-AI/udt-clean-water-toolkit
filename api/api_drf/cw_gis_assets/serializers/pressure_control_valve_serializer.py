from cwageodjango.assets.models import PressureControlValve
from rest_framework import serializers
from config.serializers import BaseGeoJsonSerializer


class PressureControlValveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PressureControlValve
        fields = ["tag", "geometry", "dmas", "modified_at", "created_at"]


class PressureControlValveGeoJsonSerializer(BaseGeoJsonSerializer):
    class Meta:
        model = PressureControlValve
        fields = ["geojson"]
