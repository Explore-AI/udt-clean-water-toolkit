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
    Intersection,
)
from cleanwater.data_managers import GeoDjangoDataManager
from cwa_geod.assets.models import *
from cwa_geod.core.db.models.functions import LineStartPoint, LineEndPoint


class MainsController(ABC, GeoDjangoDataManager):
    """This is an abstract base class and should not be
    instantiated explicitly.
    """

    WITHIN_DISTANCE = 0.5
    default_properties = [
        "id",
        "gid",
    ]  # should not include the geometry column as per convention

    def __init__(self, model):
        self.model = model

    def generate_dwithin_subquery(
        self,
        qs,
        json_fields,
        geometry_field="geometry",
        inner_subqueries={},
        extra_json_fields={},
    ):
        """
        Generates a subquery where the inner query is filtered if its geometery object
        is within the geometry of the outer query.

        Params:
              qs (Queryset, required)
              json_fields (dict, required) - A dictionary of model fields to return
              geometry_field (str, optional, default="geometry") - The field name of the outer geometry object

        Returns:
              subquery (Queryset)

        """

        subquery = qs.filter(
            geometry__dwithin=(OuterRef(geometry_field), D(m=self.WITHIN_DISTANCE))
        ).values(
            json=JSONObject(
                **json_fields,
                **extra_json_fields,
                **inner_subqueries,
                asset_name=Value(qs.model.AssetMeta.asset_name),
                asset_label=Value(qs.model.__name__)
            )
        )

        return subquery

    def _generate_dwithin_inner_subquery(self, qs, field, geometry_field="geometry"):
        inner_subquery = qs.filter(
            geometry__dwithin=(OuterRef(geometry_field), D(m=self.WITHIN_DISTANCE))
        ).values_list(field, flat=True)

        return ArraySubquery(inner_subquery)

    @staticmethod
    def generate_touches_subquery(qs, json_fields, geometry_field="geometry"):
        """
        Generates a subquery where the inner query is filtered if its geometery object
        touches the geometry of the outer query.

        Params:
               qs (Queryset, required)
               json_fields (dict, required) - A dictionary of model fields to return
               geometry_field (str, optional, default="geometry") - The field name of the outer geometry object

        Returns:
              subquery (Queryset)

        """

        subquery = qs.filter(geometry__touches=OuterRef(geometry_field)).values(
            json=JSONObject(
                **json_fields,
                asset_name=Value(qs.model.AssetMeta.asset_name),
                asset_label=Value(qs.model.__name__)
            ),
        )

        return subquery

    def generate_termini_subqueries(self, querysets):
        start_point_subqueries = []
        end_point_subqueries = []

        for qs in querysets:
            subquery1 = qs.filter(
                geometry__touches=OuterRef("start_point_geom")
            ).values(json=JSONObject(gids=ArrayAgg("gid"), ids=ArrayAgg("id")))
            subquery2 = qs.filter(geometry__touches=OuterRef("end_point_geom")).values(
                json=JSONObject(gids=ArrayAgg("gid"), ids=ArrayAgg("id"))
            )
            start_point_subqueries.append(subquery1)
            end_point_subqueries.append(subquery2)

        subquery_line_start = start_point_subqueries[0].union(
            *start_point_subqueries[0:]
        )

        subquery_line_end = end_point_subqueries[0].union(*end_point_subqueries[0:])

        return subquery_line_start, subquery_line_end

    @staticmethod
    def get_asset_json_fields(geometry_field="geometry"):
        """Overwrite the fields retrieved by the subqueries or
        the SQL functions used to retrieve them.

        Params:
              geometry_field (str, optional, defaut="geometry")

        Returns:
              json object for use in subquery
        """

        return {
            "id": "id",
            "gid": "gid",
            "geometry": geometry_field,
            "wkt": AsWKT(geometry_field),
            "dma_ids": ArrayAgg("dmas"),
            "dma_codes": ArrayAgg("dmas__code"),
            "dma_names": ArrayAgg("dmas__name"),
            "utilities": ArrayAgg("dmas__utility__name"),
        }

    @staticmethod
    def get_pipe_json_fields():
        """Overwrite the fields retrieved by the subqueries or
        the SQL functions used to retrieve them.

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
            "start_point_geom": LineStartPoint("geometry"),
            "end_point_geom": LineEndPoint("geometry"),
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
        subquery3 = self.generate_dwithin_subquery(Logger.objects.all(), json_fields)

        subquery4 = self.generate_dwithin_subquery(
            Hydrant.objects.all(),
            json_fields,
            extra_json_fields={"acoustic_logger": "acoustic_logger"},
        )

        subquery5 = self.generate_dwithin_subquery(
            PressureFitting.objects.all(),
            json_fields,
            extra_json_fields={"subtype": "subtype"},
        )

        subquery6 = self.generate_dwithin_subquery(
            PressureControlValve.objects.all(),
            json_fields,
            extra_json_fields={"subtype": "subtype"},
        )
        subquery7 = self.generate_dwithin_subquery(
            NetworkMeter.objects.all(),
            json_fields,
            extra_json_fields={"subtype": "subtype"},
        )

        subquery8 = self.generate_dwithin_subquery(Chamber.objects.all(), json_fields)

        subquery9 = self.generate_dwithin_subquery(
            OperationalSite.objects.all(),
            json_fields,
            extra_json_fields={"subtype": "subtype"},
        )

        subquery10 = self.generate_dwithin_subquery(
            NetworkOptValve.objects.all(),
            json_fields,
            extra_json_fields={"acoustic_logger": "acoustic_logger"},
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
        qs = self.model.objects.prefetch_related("dmas", "dmas__utility")
        # .filter(
        #     dmas__code__in=["ZWAL4801", "ZCHESS12", "ZCHIPO01"]
        # )

        qs = qs.annotate(
            asset_name=Value(self.model.AssetMeta.asset_name),
            asset_label=Value(qs.model.__name__),
            pipe_length=Length("geometry"),
            wkt=AsWKT("geometry"),
            dma_ids=ArrayAgg("dmas"),
            dma_codes=ArrayAgg("dmas__code"),
            dma_names=ArrayAgg("dmas__name"),
            start_point_geom=LineStartPoint("geometry"),
            end_point_geom=LineEndPoint("geometry"),
            utility_names=ArrayAgg("dmas__utility__name"),
        )

        qs = qs.annotate(**mains_intersection_subqueries, **asset_subqueries)

        return qs

    # Refs on how the GeoJSON is constructed.
    # AsGeoJson query combined with json to build object
    # https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/expressions/
    # https://postgis.net/docs/ST_AsGeoJSON.html
    # https://dakdeniz.medium.com/increase-django-geojson-serialization-performance-7cd8cb66e366
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
