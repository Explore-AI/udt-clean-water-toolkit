from django.db import models
from .utility import Utility


class DMA(models.Model):
    code = models.CharField(max_length=10, null=False, blank=False, unique=True)
    utility = models.ForeignKey(
        Utility, on_delete=models.RESTRICT, related_name="utility_dmas"
    )
    network_repr = models.JSONField(null=True)

    def __str__(self):
        return self.code
