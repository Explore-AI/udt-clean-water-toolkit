from abc import ABC, abstractmethod
from django.db.models import Value, JSONField, OuterRef
from django.db.models.functions import JSONObject
from django.contrib.gis.db import models
from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models.query import QuerySet
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import (
    AsGeoJSON,
    Cast,
    Length,
    AsWKT,
    Transform,
)
from cleanwater.controllers import GeoDjangoController
from cwa_geod.assets.models import *
from cwa_geod.core.db.models.functions.line_points import LineStartPoint, LineEndPoint


class MainsController(ABC, GeoDjangoController):
    """This is an abstract base class and should not be
    instantiated explicitly
    """

    WITHIN_DISTANCE = 0.5
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

    @staticmethod
    def get_asset_json_fields():
        """Overwrite this function to bypass
        the custom PostgreSQL functions

        Params:
              None

        Returns:
              json object for use in subquery
        """

        return {
            "id": "id",
            "gid": "gid",
            "geometry": "geometry",
            "wkt": AsWKT("geometry"),
            "geom_4326": Transform("geometry", 4326),
            "dma_ids": ArrayAgg("dmas"),
            "dma_codes": ArrayAgg("dmas__code"),
            "dma_names": ArrayAgg("dmas__name"),
            "utilities": ArrayAgg("dmas__utility__name"),
        }

    @staticmethod
    def get_pipe_json_fields():
        """Overwrite this function to bypass
        the custom PostgreSQL functions

        Params:
              None

        Returns:
              json object for use in subquery
        """

        return {
            "id": "id",
            "gid": "gid",
            "geometry": "geometry",
            "wkt": AsWKT("geometry"),
            "start_geom_4326": Transform(LineStartPoint("geometry"), 4326),
            "end_geom_4326": Transform(LineEndPoint("geometry"), 4326),
            "dma_ids": ArrayAgg("dmas"),
            "dma_codes": ArrayAgg("dmas__code"),
            "dma_names": ArrayAgg("dmas__name"),
            "utilities": ArrayAgg("dmas__utility__name"),
        }

    @abstractmethod
    def _generate_mains_subqueries(self):
        raise NotImplementedError(
            "Function should be defined in the child class and not called explicitly. "
        )

    def _generate_asset_subqueries(self):
        json_fields = self.get_asset_json_fields()

        # This section is deliberately left verbose for clarity
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
            "logger_data": ArraySubquery(subquery3),
            "hydrant_data": ArraySubquery(subquery4),
            "pressure_fitting_data": ArraySubquery(subquery5),
            "pressure_valve_data": ArraySubquery(subquery6),
            "network_meter_data": ArraySubquery(subquery7),
            "chamber_data": ArraySubquery(subquery8),
            "operational_site_data": ArraySubquery(subquery9),
            "network_opt_valve": ArraySubquery(subquery10),
        }
        return subqueries

    def get_pipe_point_relation_queryset(self):
        mains_intersection_subqueries = self._generate_mains_subqueries()
        asset_subqueries = self._generate_asset_subqueries()

        # https://stackoverflow.com/questions/51102389/django-return-array-in-subquery
        qs = self.model.objects.prefetch_related("dmas", "dmas__utility").annotate(
            asset_name=Value(self.model.AssetMeta.asset_name),
            length=Length("geometry"),
            wkt=AsWKT("geometry"),
            dma_ids=ArrayAgg("dmas"),
            dma_codes=ArrayAgg("dmas__code"),
            dma_names=ArrayAgg("dmas__name"),
            utility_names=ArrayAgg("dmas__utility__name"),
            **mains_intersection_subqueries,
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

    def mains_to_geojson(self, properties=None):
        """Serialization of db data to GeoJSON.

        Faster (with bigger datasets) serialization into geoson.

        Params:
                properties: list (optional). A list of model fields
        Returns:
                geoJSON: geoJSON object of DistributionMains
        """

        qs = self.get_geometry_queryset(properties)
        return self.queryset_to_geojson(qs)

    def mains_to_geojson2(self, properties=None):
        """Faster (with bigger datasets) serialization into geoson.

        Params:
                properties: list (optional). A list of model fields
        Returns:
                geoJSON: geoJSON object of Mains
        """

        qs = self.get_geometry_queryset(properties)
        return self.queryset_to_geojson(qs)

    def mains_to_geodataframe(self, properties=None):
        """Serialization of db data to GeoJSON.

        Faster (with bigger datasets) serialization into geoson.

        Params:
                properties: list (optional). A list of model fields
        Returns:
                geoJSON: geoJSON object of Mains
        """

        qs = self.get_geometry_queryset(properties)
        return self.queryset_to_geodataframe(qs)
