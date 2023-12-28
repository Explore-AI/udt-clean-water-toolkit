from django.contrib.gis.db import models
from cwa_geod.utilities.models.dma import DMA
from cwa_geod.config.settings import DEFAULT_SRID


class Logger(models.Model):
    gisid = models.IntegerField(null=False, blank=False, unique=True)
    shape_x = models.FloatField(null=False, blank=False)
    shape_y = models.FloatField(null=False, blank=False)
    geometry = models.PointField(
        spatial_index=True, null=False, blank=False, srid=DEFAULT_SRID
    )
    dma = models.ForeignKey(DMA, on_delete=models.CASCADE, related_name="dma_loggers")
