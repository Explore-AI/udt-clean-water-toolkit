from django.contrib.gis.db.models.functions import AsGeoJSON, Cast
from django.db.models.functions import JSONObject
from django.db.models import Value, JSONField, OuterRef
from django.contrib.gis.measure import D
from django.contrib.postgres.expressions import ArraySubquery
from cleanwater.controllers import GeoDjangoController
from cwa_geod.assets.models import (
    Logger,
    TrunkMain,
    Hydrant,
    PressureFitting,
    PressureControlValve,
    Chamber,
    NetworkMeter,
)
from cwa_geod.config.settings import DEFAULT_SRID


class TrunkMainsController(GeoDjangoController):
    """Convert trunk_mains data to geoJSON. Please look into
    structore of geoJSON object. Also, see these refs
    for a guide on how the geojson is contructed.

    AsGeoJson query combined with json to build object

    https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/expressions/
    https://postgis.net/docs/ST_AsGeoJSON.html
    https://dakdeniz.medium.com/increase-django-geojson-serialization-performance-7cd8cb66e366
    """

    model = TrunkMain
    srid = DEFAULT_SRID
    # items_limit = 100000  # TODO: set default in config
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
        ).values(json=JSONObject(**json_fields))
        return subquery

    def _generate_touches_subquery(self, qs, json_fields, geometry_field="geometry"):
        subquery = qs.filter(geometry__touches=OuterRef(geometry_field)).values(
            json=JSONObject(**json_fields)
        )
        return subquery

    def _generate_single_dma_asset_subqueries(self):
        json_fields = {
            "id": "id",
            "gisid": "gisid",
            "geometry": "geometry",
            "dma_id": "dma",
            "dma_code": "dma__code",
        }

        subquery1 = self._generate_touches_subquery(
            self.model.objects.all(), json_fields
        )
        subquery2 = self._generate_dwithin_subquery(Logger.objects.all(), json_fields)
        subquery3 = self._generate_dwithin_subquery(Hydrant.objects.all(), json_fields)
        subquery4 = self._generate_dwithin_subquery(
            PressureFitting.objects.all(), json_fields
        )

        subqueries = {
            "trunk_mains_data": subquery1,
            "logger_data": subquery2,
            "hydrant_data": subquery3,
            "pressure_fitting_data": subquery4,
        }
        return subqueries

    def _generate_two_dma_asset_subqueries(self):
        json_fields = {
            "id": "id",
            "gisid": "gisid",
            "geometry": "geometry",
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
            "pressure_valve_data": subquery1,
            "network_meter_data": subquery2,
        }

        return subqueries

    def get_relation_to_point_assets_queryset(self):
        single_dma_asset_subqueries = self._generate_single_dma_asset_subqueries()
        two_dma_asset_subqueries = self._generate_two_dma_asset_subqueries()

        subquery7 = Chamber.objects.filter(
            geometry__dwithin=(OuterRef("geometry"), D(m=1))
        ).values(
            json=JSONObject(
                id="id",
                gisid="gisid",
                geometry="geometry",
            )
        )

        # https://stackoverflow.com/questions/51102389/django-return-array-in-subquery
        qs = self.model.objects.annotate(
            **single_dma_asset_subqueries,
            **two_dma_asset_subqueries,
            chamber_data=ArraySubquery(subquery7),
        )

        import pdb

        pdb.set_trace()

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

    def trunk_mains_to_geojson(self, properties=None):
        """Serialization of db data to GeoJSON.

        Faster (with bigger datasets) serialization into geoson.

        Params:
              properties: list (optional). A list of model fields
        Returns:
              geoJSON: geoJSON object
        """

        qs = self.get_geometry_queryset(properties)
        return self.queryset_to_geojson(qs)

    def trunk_mains_to_geojson2(self, properties=None):
        """Serialization of db data to GeoJSON. Alternate method
        Slighly faster serialization into geoson compared to 1) for smaller
        data sets but employs iteration.

        Params:
              properties: list (optional). A list of model fields
        Returns:
              geoJSON: geoJSON object
        """
        properties = properties or self.default_properties
        properties = set(properties)
        json_properties = dict(zip(properties, properties))

        qs = self.model.objects.values(*properties).annotate(
            properties=JSONObject(**json_properties),
            geometry=AsGeoJSON("geometry", crs=True),
        )
        return self.queryset_to_geojson2(qs)

    def trunk_mains_to_geodataframe(self, properties=None):
        """Serialization of db data to GeoPandas DataFrame.

        Params:
              properties: list (optional). A list of model fields
        Returns:
              geoJSON: geoJSON object
        """

        qs = self.get_geometry_queryset(properties)
        return self.django_queryset_to_geodataframe(qs)

    # 1) slower serialization into geojson
    # start = datetime.datetime.now()
    # trunk_mains = TrunkMain.objects.all()
    # trunk_mains_data = serialize(
    #     "geojson", trunk_mains, geometry_field="geometry", srid=DEFAULT_SRID
    # )
    # finish = datetime.datetime.now()
    # print(finish - start)
    # trunk_mains_gdf = gpd.read_file(trunk_mains_data)
