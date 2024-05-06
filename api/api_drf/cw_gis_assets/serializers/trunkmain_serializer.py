from rest_framework import serializers
from cwageodjango.assets.models.trunk_main import TrunkMain
from config.serializers import BaseGeoJsonSerializer


class TrunkMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrunkMain
        fields = ["gid", "geometry", "dmas", "modified_at", "created_at"]
        read_only_fields = ("id",)


class TrunkMainGeoJsonSerializer(BaseGeoJsonSerializer):

    class Meta:
        model = TrunkMain
        fields = ["geojson"]
