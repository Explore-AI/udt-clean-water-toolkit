from cwageodjango.assets.models import NetworkMeter
from rest_framework import serializers
from config.serializers import BaseGeoJsonSerializer


class NetworkMeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkMeter
        fields = ["tag", "geometry", "dmas", "modified_at", "created_at"]


class NetworkMeterGeoJsonSerializer(BaseGeoJsonSerializer):
    class Meta:
        model = NetworkMeter
        fields = ["geojson"]
