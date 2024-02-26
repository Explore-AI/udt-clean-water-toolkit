from django.contrib.gis.db import models
from cwa_geod.utilities.models.dma import DMA
from cwa_geod.config.settings import DEFAULT_SRID


class DistributionMain(models.Model):
    gisid = models.IntegerField(null=False, blank=False, unique=True)
    geometry = models.MultiLineStringField(
        spatial_index=True, null=False, blank=False, srid=DEFAULT_SRID
    )
    dma = models.ManyToManyField(
        DMA, on_delete=models.RESTRICT, related_name="dma_distribution_mains"
    )
