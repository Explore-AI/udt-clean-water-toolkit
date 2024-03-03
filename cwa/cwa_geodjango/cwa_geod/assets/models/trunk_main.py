from django.contrib.gis.db import models
from cwa_geod.utilities.models import DMA
from cwa_geod.core.constants import DEFAULT_SRID, TRUNK_MAIN__NAME


class TrunkMain(models.Model):
    gid = models.IntegerField(null=False, blank=False, unique=True)
    geometry = models.MultiLineStringField(
        spatial_index=True, null=False, blank=False, srid=DEFAULT_SRID
    )
    dmas = models.ManyToManyField(DMA, related_name="dma_trunk_mains")
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class AssetMeta:
        asset_name = TRUNK_MAIN__NAME
