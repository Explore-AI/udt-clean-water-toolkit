from cleanwater.controllers.network_controller import NetworkController
from cwa_geod.assets.controllers import TrunkMainsController
from cwa_geod.assets.controllers import DistributionMainsController
from cwa_geod.config.settings import DEFAULT_SRID


class GisToGraphNetwork(NetworkController):
    """Create a graph network of assets from a geospatial
    network of assets"""

    def __init__(self, srid=None):
        self.srid = srid or DEFAULT_SRID
        super().__init__(self.srid)

    def create_network(self):
        trunk_mains_nx = self._create_trunk_mains_graph()

        # TODO: geospatial join on all the node assets
        # TODO: add the nodes to the graph

        return trunk_mains_nx

    def create_network2(self):
        from django.contrib.gis.measure import D
        from django.contrib.postgres.expressions import ArraySubquery
        from django.db.models.functions import JSONObject
        from cwa_geod.assets.models import (
            Logger,
            TrunkMain,
            Hydrant,
            PressureFitting,
            PressureControlValve,
        )

        # https://stackoverflow.com/questions/51102389/django-return-array-in-subquery
        subquery1 = TrunkMain.objects.filter(
            geometry__touches=OuterRef("geometry")
        ).values(
            json=JSONObject(
                id="id",
                gisid="gisid",
                geometry="geometry",
                dma_id="dma",
                dma_code="dma__code",
            )
        )

        subquery2 = Logger.objects.filter(
            geometry__dwithin=(OuterRef("geometry"), D(m=1))
        ).values(
            json=JSONObject(
                id="id",
                gisid="gisid",
                geometry="geometry",
                dma_id="dma",
                dma_code="dma__code",
            )
        )

        subquery3 = Hydrant.objects.filter(
            geometry__dwithin=(OuterRef("geometry"), D(m=1))
        ).values(
            json=JSONObject(
                id="id",
                gisid="gisid",
                geometry="geometry",
                dma_id="dma",
                dma_code="dma__code",
            )
        )

        qs = TrunkMain.objects.annotate(
            trunk_mains_data=ArraySubquery(subquery1),
            logger_data=ArraySubquery(subquery2),
            hydrant_data=ArraySubquery(subquery3),
        )

        import pdb

        pdb.set_trace()

    def _create_trunk_mains_graph(self):
        tm = TrunkMainsController()

        # TODO: union querysets
        # dm = DistributionMainsController()

        trunk_mains = tm.get_geometry_queryset()
        return self.create_pipes_network(trunk_mains)
