from rest_framework import serializers
from cwageodjango.utilities.models import DMA


class DmaSerializer(serializers.ModelSerializer):

    value = serializers.CharField(source="code", read_only=True)

    class Meta:
        model = DMA
        fields = ["id", "code", "name", "modified_at", "created_at", "value"]
        read_only_fields = ["id"]
