from django.contrib.gis.db import models
from cwageodjango.utilities.models import DMA
from cwageodjango.core.constants import DEFAULT_SRID, DISTRIBUTION_MAIN__NAME


class DistributionMain(models.Model):
    gid = models.IntegerField(null=False, blank=False, unique=True, db_index=True)
    geometry = models.LineStringField(
        spatial_index=True, null=False, blank=False, srid=DEFAULT_SRID
    )
    geometry_4326 = models.LineStringField(
        spatial_index=True, null=False, blank=False, srid=4326
    )
    dmas = models.ManyToManyField(DMA, related_name="dma_distribution_mains")
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        ordering = ["dmas__id"]

    class AssetMeta:
        asset_name = DISTRIBUTION_MAIN__NAME
