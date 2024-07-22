from rest_framework import serializers
from cwageodjango.waterpipes.models import PipeFlow


class PipeFlowSerializer(serializers.ModelSerializer):

    class Meta:
        model = PipeFlow
        fields = ["pipe_main", "flow_data"]
