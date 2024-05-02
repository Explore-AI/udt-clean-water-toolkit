from rest_framework import serializers
from cwageodjango.assets.models.trunk_main import TrunkMain
import json


class TrunkMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrunkMain
        fields = ["gid", "geometry", "dmas", "modified_at", "created_at"]
        read_only_fields = ("id",)


class TrunkMainGeoJsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrunkMain
        fields = ["gid", "geometry"]
        read_only_fields = ("id",)

    def to_representation(self, instance, srid):
        srid: int | None = srid

        # geo_data: dict = {
        #     "type": "FeatureCollection",
        #     "crs": {"type": "name", "properties": {"name": f"EPSG:{srid}"}},
        #     "features": list(qs),
        # }
        # return json.dumps(geo_data)

        geo_data: dict = {
            "type": "Feature",
            # "crs": {"type": "name", "properties": {"name": f"EPSG:{srid}"}},
            "properties": {
                "gid": instance.gid
            },
            "geometry": json.loads(instance.geometry),
        }

        return geo_data
