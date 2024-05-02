from rest_framework import serializers
from cwageodjango.assets.models.trunk_main import TrunkMain


class TrunkMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrunkMain
        fields = ["gid", "geometry", "dmas", "modified_at", "created_at"]
        read_only_fields = ("id",)
