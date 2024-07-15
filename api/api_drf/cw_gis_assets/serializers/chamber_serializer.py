from rest_framework import serializers
from cwageodjango.assets.models.chamber import Chamber
from config.serializers import BaseGeoJsonSerializer


class ChamberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamber
        fields = ["gid", "geometry", "dmas", "modified_at", "created_at"]
        read_only_fields = ["id"]


class ChamberGeoJsonSerializer(BaseGeoJsonSerializer):
    class Meta:
        model = Chamber
        fields = ["geojson"]
