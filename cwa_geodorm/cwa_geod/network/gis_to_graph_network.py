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

    def _generate_dwithin_subquery(self, model, json_fields):
        from django.contrib.gis.measure import D
        from django.db.models.functions import JSONObject
        from django.db.models import OuterRef

        subquery = model.objects.filter(
            geometry__dwithin=(OuterRef("geometry"), D(m=1))
        ).values(json=JSONObject(**json_fields))
        return subquery

    def _generate_touches_subquery(self, model, json_fields):
        from django.contrib.gis.measure import D
        from django.db.models.functions import JSONObject
        from django.db.models import OuterRef

        subquery = model.objects.filter(geometry__touches=OuterRef("geometry")).values(
            json=JSONObject(**json_fields)
        )
        return subquery

    def create_network2(self):
        from django.contrib.gis.measure import D
        from django.contrib.postgres.expressions import ArraySubquery
        from django.db.models import OuterRef
        from django.db.models.functions import JSONObject
        from cwa_geod.assets.models import (
            Logger,
            TrunkMain,
            Hydrant,
            PressureFitting,
            PressureControlValve,
            Chamber,
        )

        json_fields = {
            "id": "id",
            "gisid": "gisid",
            "geometry": "geometry",
            "dma_id": "dma",
            "dma_code": "dma__code",
        }

        # https://stackoverflow.com/questions/51102389/django-return-array-in-subquery
        subquery1 = self._generate_touches_subquery(TrunkMain, json_fields):
        subquery2 = self._generate_dwithin_subquery(Logger, json_fields)
        subquery3 = self._generate_dwithin_subquery(Hydrant, json_fields)
        subquery4 = self._generate_dwithin_subquery(PressureFitting, json_fields)

        subquery5 = PressureControlValve.objects.filter(
            geometry__dwithin=(OuterRef("geometry"), D(m=1))
        ).values(
            json=JSONObject(
                id="id",
                gisid="gisid",
                geometry="geometry",
                dma_1_id="dma_1",
                dma_2_id="dma_2",
                dma_1_code="dma_1__code",
                dma_2_code="dma_1__code",
            )
        )

        subquery6 = Chamber.objects.filter(
            geometry__dwithin=(OuterRef("geometry"), D(m=1))
        ).values(
            json=JSONObject(
                id="id",
                gisid="gisid",
                geometry="geometry",
            )
        )

        qs = TrunkMain.objects.annotate(
            trunk_mains_data=ArraySubquery(subquery1),
            logger_data=ArraySubquery(subquery2),
            hydrant_data=ArraySubquery(subquery3),
            pressure_fitting_data=ArraySubquery(subquery4),
            pressure_valve_data=ArraySubquery(subquery5),
            chamber_data=ArraySubquery(subquery6),
        )

        import pdb

        pdb.set_trace()

    def _create_trunk_mains_graph(self):
        tm = TrunkMainsController()

        # TODO: union querysets
        # dm = DistributionMainsController()

        trunk_mains = tm.get_geometry_queryset()
        return self.create_pipes_network(trunk_mains)
