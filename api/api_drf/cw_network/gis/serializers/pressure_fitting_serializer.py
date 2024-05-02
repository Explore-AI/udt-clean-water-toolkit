from cwageodjango.assets.models import PressureFitting
from rest_framework import serializers


class PressureFittingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PressureFitting
        fields = ["gid", "geometry", "dmas", "modified_at", "created_at"]
