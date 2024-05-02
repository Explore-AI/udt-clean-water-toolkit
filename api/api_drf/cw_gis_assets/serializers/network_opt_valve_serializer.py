from cwageodjango.assets.models import NetworkOptValve
from rest_framework import serializers


class NetworkOptValveSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkOptValve
        fields = ["gid", "geometry", "dmas", "modified_at", "created_at"]
