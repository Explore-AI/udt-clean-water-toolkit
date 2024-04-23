from django.contrib.gis.db import models
from cwa_geod.utilities.models import DMA
from cwa_geod.core.constants import DEFAULT_SRID, NETWORK_OPT_VALVE__NAME


class NetworkOptValve(models.Model):
    gid = models.IntegerField(null=False, blank=False, unique=True, db_index=True)
    acoustic_logger = models.BooleanField(null=False, blank=False)
    geometry = models.PointField(
        spatial_index=True, null=False, blank=False, srid=DEFAULT_SRID
    )
    # geometry_4326 = models.PointField(
    #     spatial_index=True, null=False, blank=False, srid=4326
    # )
    dmas = models.ManyToManyField(DMA, related_name="dma_network_opt_valves")
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class AssetMeta:
        asset_name = NETWORK_OPT_VALVE__NAME
