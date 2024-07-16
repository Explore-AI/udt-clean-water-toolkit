from django.contrib.gis.db import models
from cwageodjango.assets.models import PipeMain


class PipeFlow(models.Model):
    pipe_main = models.ForeignKey(
        PipeMain, on_delete=models.CASCADE, related_name="flows"
    )
    flow_data = models.JSONField()
