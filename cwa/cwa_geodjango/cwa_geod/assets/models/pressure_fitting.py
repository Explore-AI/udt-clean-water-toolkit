from django.contrib.gis.db import models
from cwa_geod.utilities.models import DMA
from cwa_geod.config.settings import DEFAULT_SRID


class PressureFitting(models.Model):
    gid = models.IntegerField(null=False, blank=False, unique=True)
    geometry = models.PointField(
        spatial_index=True, null=False, blank=False, srid=DEFAULT_SRID
    )
    dma = models.ManyToManyField(DMA, related_name="dma_pressure_fittings")
