from django.contrib.gis.db import models
from ...utilities.models.dma import DMA
from ...config.settings import DEFAULT_SRID


class TrunkMain(models.Model):
    gisid = models.IntegerField(null=False, blank=False, unique=True)
    shape_length = models.FloatField(null=False, blank=False)
    geometry = models.MultiLineStringField(
        spatial_index=True, null=False, blank=False, srid=DEFAULT_SRID
    )
    dma = models.ForeignKey(
        DMA, on_delete=models.CASCADE, related_name="dma_trunk_mains"
    )
