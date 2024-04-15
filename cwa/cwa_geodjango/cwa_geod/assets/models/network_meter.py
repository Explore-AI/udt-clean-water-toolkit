from django.contrib.gis.db import models
from cwa_geod.utilities.models import DMA
from cwa_geod.core.constants import DEFAULT_SRID, NETWORK_METER_NAME


class NetworkMeter(models.Model):
    gid = models.IntegerField(null=False, blank=False, unique=True, db_index=True)
    #hsi_id = models.IntegerField(null=False, blank=False, unique=True)
    #tag_name = models.CharField(null=False, blank=False, unique=True)

    geometry = models.PointField(
        spatial_index=True, null=False, blank=False, srid=DEFAULT_SRID
    )
    subtype = models.CharField(null=False, blank=False)
    dmas = models.ManyToManyField(DMA, related_name="dma_network_meters")
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class AssetMeta:
        asset_name = NETWORK_METER_NAME
