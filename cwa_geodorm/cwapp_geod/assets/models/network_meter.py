from django.contrib.gis.db import models
from ...utilities.models.dma import DMA
from ...config.settings import DEFAULT_SRID


class NetworkMeter(models.Model):
    gisid = models.IntegerField(null=False, blank=False, unique=True)
    shape_x = models.FloatField(null=False, blank=False)
    shape_y = models.FloatField(null=False, blank=False)
    geometry = models.PointField(
        spatial_index=True, null=False, blank=False, srid=DEFAULT_SRID
    )
    dma_1 = models.ForeignKey(
        DMA, on_delete=models.CASCADE, related_name="dma_1_network_meters"
    )
    dma_2 = models.ForeignKey(
        DMA, on_delete=models.CASCADE, related_name="dma_2_network_meters"
    )
