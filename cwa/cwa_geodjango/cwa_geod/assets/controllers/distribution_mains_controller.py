from django.contrib.gis.db.models.functions import AsGeoJSON, Cast
from django.db.models.functions import JSONObject
from django.db.models import Value, JSONField, OuterRef
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Length, AsWKT
from django.contrib.postgres.expressions import ArraySubquery
from cleanwater.controllers import GeoDjangoController
from cwa_geod.assets.models import (
    Logger,
    TrunkMain,
    DistributionMain,
    Hydrant,
    PressureFitting,
    PressureControlValve,
    OperationalSite,
    Chamber,
    NetworkMeter,
)
from cwa_geod.config.settings import DEFAULT_SRID


class DistributionMainsController(GeoDjangoController):
    """Convert distribution_mains data to GeoJson. Please look into
    structore of GeoJson object. Also, see these refs
    for a guide on how the GeoJson is contructed.

    AsGeoJson query combined with json to build object

    https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/expressions/
    https://postgis.net/docs/ST_AsGeoJSON.html
    https://dakdeniz.medium.com/increase-django-geojson-serialization-performance-7cd8cb66e366
    """

    model = DistributionMain
    srid = DEFAULT_SRID
    items_limit = 2000000  # set default in cofig
    default_properties = [
        "id",
        "gisid",
        "shape_length",
        "dma_id",
        "dma__code",
    ]  # should not include the geometry column as per convention

    def _generate_dwithin_subquery(self, qs, json_fields, geometry_field="geometry"):
        subquery = qs.filter(
            geometry__dwithin=(OuterRef(geometry_field), D(m=1))
        ).values(
            json=JSONObject(**json_fields, asset_model_name=Value(qs.model.__name__))
        )
        return subquery

    def _generate_touches_subquery(self, qs, json_fields, geometry_field="geometry"):
        subquery = qs.filter(geometry__touches=OuterRef(geometry_field)).values(
            json=JSONObject(**json_fields, asset_model_name=Value(qs.model.__name__))
        )
        return subquery

    def _generate_no_dma_asset_subqueries(self):
        json_fields = {
            "id": "id",
            "gisid": "gisid",
            "geometry": "geometry",
            "wkt": AsWKT("geometry"),
        }

        subquery1 = self._generate_dwithin_subquery(Chamber.objects.all(), json_fields)
        subquery2 = self._generate_dwithin_subquery(
            OperationalSite.objects.all(), json_fields
        )

        subqueries = {
            "chamber_data": ArraySubquery(subquery1),
            "operational_site_data": ArraySubquery(subquery2),
        }
        return subqueries

    def _generate_single_dma_asset_subqueries(self):
        json_fields = {
            "id": "id",
            "gisid": "gisid",
            "geometry": "geometry",
            "wkt": AsWKT("geometry"),
            "dma_id": "dma",
            "dma_code": "dma__code",
        }

        subquery1 = self._generate_touches_subquery(
            self.model.objects.all(), json_fields
        )
        subquery2 = self._generate_touches_subquery(
            TrunkMain.objects.all(), json_fields
        )
        subquery3 = self._generate_dwithin_subquery(Logger.objects.all(), json_fields)
        subquery4 = self._generate_dwithin_subquery(Hydrant.objects.all(), json_fields)
        subquery5 = self._generate_dwithin_subquery(
            PressureFitting.objects.all(), json_fields
        )

        subqueries = {
            "distribution_mains_data": ArraySubquery(subquery1),
            "trunk_mains_data": ArraySubquery(subquery2),
            "logger_data": ArraySubquery(subquery3),
            "hydrant_data": ArraySubquery(subquery4),
            "pressure_fitting_data": ArraySubquery(subquery5),
        }
        return subqueries

    def _generate_two_dma_asset_subqueries(self):
        json_fields = {
            "id": "id",
            "gisid": "gisid",
            "geometry": "geometry",
            "wkt": AsWKT("geometry"),
            "dma_1_id": "dma_1",
            "dma_2_id": "dma_2",
            "dma_1_code": "dma_1__code",
            "dma_2_code": "dma_1__code",
        }

        subquery1 = self._generate_dwithin_subquery(
            PressureControlValve.objects.all(), json_fields
        )
        subquery2 = self._generate_dwithin_subquery(
            NetworkMeter.objects.all(), json_fields
        )

        subqueries = {
            "pressure_valve_data": ArraySubquery(subquery1),
            "network_meter_data": ArraySubquery(subquery2),
        }

        return subqueries

    def get_pipe_point_relation_queryset(self):
        no_dma_asset_subqueries = self._generate_no_dma_asset_subqueries()
        single_dma_asset_subqueries = self._generate_single_dma_asset_subqueries()
        two_dma_asset_subqueries = self._generate_two_dma_asset_subqueries()

        # https://stackoverflow.com/questions/51102389/django-return-array-in-subquery
        qs = self.model.objects.select_related("dma").annotate(
            asset_model_name=Value("DistributionMain"),
            length=Length("geometry"),
            wkt=AsWKT("geometry"),
            **no_dma_asset_subqueries,
            **single_dma_asset_subqueries,
            **two_dma_asset_subqueries,
        )

        return qs

    def get_geometry_queryset(self, properties=None):
        properties = properties or self.default_properties
        properties = set(properties)
        json_properties = dict(zip(properties, properties))

        qs = (
            self.model.objects.values(*properties)
            .annotate(
                geojson=JSONObject(
                    properties=JSONObject(**json_properties),
                    type=Value("Feature"),
                    geometry=Cast(
                        AsGeoJSON("geometry", crs=True),
                        output_field=JSONField(),
                    ),
                ),
            )
            .values_list("geojson", flat=True)
        )
        return qs

    def distribution_mains_to_geojson(self, properties=None):
        """Serialization of db data to GeoJSON.

        Fast (maybe with bigger datasets) serialization into geoson.

        Params:
              properties: list (optional). A list of model fields
        Returns:
              geoJSON: geoJSON object
        """

        qs = self.get_geometry_queryset(properties)
        return self.queryset_to_geojson(qs)
