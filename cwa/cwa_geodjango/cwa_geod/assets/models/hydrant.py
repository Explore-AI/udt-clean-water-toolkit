from django.contrib.gis.db import models
from cwa_geod.utilities.models import DMA
from cwa_geod.core.constants import DEFAULT_SRID, HYDRANT__NAME


class Hydrant(models.Model):
    gid = models.IntegerField(null=False, blank=False, unique=True, db_index=True)
    geometry = models.PointField(
        spatial_index=True, null=False, blank=False, srid=DEFAULT_SRID
    )
    dmas = models.ManyToManyField(DMA, related_name="dma_hydrants")
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class AssetMeta:
        asset_name = HYDRANT__NAME
