from django.db.models import Value, JSONField, OuterRef
from django.db.models.functions import JSONObject
from django.db.models.query import QuerySet
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import AsGeoJSON, Cast, Length, AsWKT
from django.contrib.postgres.expressions import ArraySubquery
from cleanwater.controllers import GeoDjangoController
from cwa_geod.assets.models import *
from cwa_geod.core.constants import DEFAULT_SRID


class DistributionMainsController(GeoDjangoController):
    """Convert distribution mains data to Queryset or GeoJSON.

    Refs on how the GeoJSON is constructed.
    AsGeoJson query combined with json to build object
    https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/expressions/
    https://postgis.net/docs/ST_AsGeoJSON.html
    https://dakdeniz.medium.com/increase-django-geojson-serialization-performance-7cd8cb66e366
    """

    model = DistributionMain
    srid = DEFAULT_SRID
    # items_limit = 100000  # TODO: set default in config
    WITHIN_DISTANCE = 1
    default_properties = [
        "id",
        "gid",
    ]  # should not include the geometry column as per convention

    def _generate_dwithin_subquery(self, qs, json_fields, geometry_field="geometry"):
        subquery = qs.filter(
            geometry__dwithin=(OuterRef(geometry_field), D(m=self.WITHIN_DISTANCE))
        ).values(
            json=JSONObject(
                **json_fields, asset_name=Value(qs.model.AssetMeta.asset_name)
            )
        )
        return subquery

    def _generate_touches_subquery(self, qs, json_fields, geometry_field="geometry"):
        subquery = qs.filter(geometry__touches=OuterRef(geometry_field)).values(
            json=JSONObject(
                **json_fields, asset_name=Value(qs.model.AssetMeta.asset_name)
            )
        )
        return subquery

    def _generate_asset_subqueries(self):
        json_fields = {
            "id": "id",
            "gid": "gid",
            "geometry": "geometry",
            "wkt": AsWKT("geometry"),
            "dmas": "dmas",
        }

        # This section is deliberately left verbose for clarity
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

        subquery6 = self._generate_dwithin_subquery(
            PressureControlValve.objects.all(), json_fields
        )
        subquery7 = self._generate_dwithin_subquery(
            NetworkMeter.objects.all(), json_fields
        )

        subquery8 = self._generate_dwithin_subquery(Chamber.objects.all(), json_fields)

        subquery9 = self._generate_dwithin_subquery(
            OperationalSite.objects.all(), json_fields
        )

        subquery10 = self._generate_dwithin_subquery(
            NetworkOptValve.objects.all(), json_fields
        )

        subqueries = {
            "trunk_mains_data": ArraySubquery(subquery1),
            "distribution_mains_data": ArraySubquery(subquery2),
            "logger_data": ArraySubquery(subquery3),
            "hydrant_data": ArraySubquery(subquery4),
            "pressure_fitting_data": ArraySubquery(subquery5),
            "pressure_valve_data": ArraySubquery(subquery6),
            "network_meter_data": ArraySubquery(subquery7),
            "chamber_data": ArraySubquery(subquery8),
            "operational_site_data": ArraySubquery(subquery9),
        }
        return subqueries

    def get_pipe_point_relation_queryset(self):
        asset_subqueries = self._generate_asset_subqueries()

        # https://stackoverflow.com/questions/51102389/django-return-array-in-subquery
        qs = self.model.objects.prefetch_related("dmas").annotate(
            asset_name=Value(self.model.AssetMeta.asset_name),
            length=Length("geometry"),
            wkt=AsWKT("geometry"),
            **asset_subqueries
        )
        return qs

    def get_geometry_queryset(self, properties=None) -> QuerySet:
        properties = properties or self.default_properties
        properties = set(properties)
        json_properties = dict(zip(properties, properties))

        qs: QuerySet = (
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

        Faster (with bigger datasets) serialization into geoson.

        Params:
              properties: list (optional). A list of model fields
        Returns:
              geoJSON: geoJSON object of DistributionMains
        """

        qs = self.get_geometry_queryset(properties)
        return self.queryset_to_geojson(qs)

    def distribution_mains_to_geojson2(self, properties=None):
        """Serialization of db data to GeoJSON. Alternate method
        Slightly faster serialization into geoson compared to distribution_mains_to_geojson()
        for smaller data sets but employs iteration.

        Params:
              properties: list (optional). A list of model fields
        Returns:
              geoJSON: geoJSON object of DistributionMains
        """
        properties = properties or self.default_properties
        properties = set(properties)
        json_properties = dict(zip(properties, properties))

        qs = self.model.objects.values(*properties).annotate(
            properties=JSONObject(**json_properties),
            geometry=AsGeoJSON("geometry", crs=True),
        )
        return self.queryset_to_geojson2(qs)

    def distribution_mains_to_geodataframe(self, properties=None):
        """Serialization of db data to GeoPandas DataFrame.

        Params:
              properties: list (optional). A list of model fields
        Returns:
              geoJSON: geoJSON object of DistributionMains
        """

        qs = self.get_geometry_queryset(properties)
        return self.django_queryset_to_geodataframe(qs)
