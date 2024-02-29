from django.contrib.gis.db import models
from .utility import Utility
from cwa_geod.core.constants import DEFAULT_SRID


class DMA(models.Model):
    code = models.CharField(max_length=10, null=False, blank=False, unique=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    utility = models.ForeignKey(
        Utility, on_delete=models.RESTRICT, related_name="utility_dmas"
    )
    network_repr = models.JSONField(null=True)
    geometry = models.MultiPolygonField(
        spatial_index=True, null=False, blank=False, srid=DEFAULT_SRID
    )
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.code
