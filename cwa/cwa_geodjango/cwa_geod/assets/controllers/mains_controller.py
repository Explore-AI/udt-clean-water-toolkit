from django.db.models import Value, JSONField, OuterRef
from django.db.models.functions import JSONObject
from django.contrib.gis.db import models
from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.expressions import ArraySubquery
from django.db.models.query import QuerySet
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import AsGeoJSON, Cast, Length, AsWKT
from cleanwater.controllers import GeoDjangoController
from cwa_geod.assets.models import *
from cwa_geod.core.constants import DEFAULT_SRID   

class MainsController(GeoDjangoController): 
    """_summary_
        Base Controller class for the Mains Controller classes
    """
    model = models.Model # model will need to be overridden for each child controller class
    srid = DEFAULT_SRID
    # items_limit = 100000  # TODO: set default in config
    WITHIN_DISTANCE = 1
    default_properties = [
        "id",
        "gid",
    ]  # should not include the geometry column as per convention
    
    # at runtime ensure that the model created by the mains controller is a TrunkMain or DistributionMain class
    # assert model in (TrunkMain, DistributionMain), "model attribute must be either a TrunkMain or DistributionMian"
    
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
    def set_json_fields():
        """Overwrite this function to bypass
        custom PostgreSQL functions

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
            "dma_ids": ArrayAgg("dmas"),
            "dma_codes": ArrayAgg("dmas__code"),
            "dma_names": ArrayAgg("dmas__name"),
        }
    
    def _generate_asset_subqueries(self):
        json_fields = self.set_json_fields()
        

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
            "distribution_mains_data": ArraySubquery(subquery1),
            "trunk_mains_data": ArraySubquery(subquery2),
            "logger_data": ArraySubquery(subquery3),
            "hydrant_data": ArraySubquery(subquery4),
            "pressure_fitting_data": ArraySubquery(subquery5),
            "pressure_valve_data": ArraySubquery(subquery6),
            "network_meter_data": ArraySubquery(subquery7),
            "chamber_data": ArraySubquery(subquery8),
            "operational_site_data": ArraySubquery(subquery9),
        }
        return subqueries
    
    def _generate_asset_subqueries2(self):
        # An attempt to improve the _generate_asset_subqueries method
        # get the json fields 
        json_fields = self.set_json_fields()

        # define the model objects
        # 1 includes all model objects except for NetworkOptValve Model
        model_objects = {
            "distribution_mains_data": self.model.objects.all(),
            "trunk_mains_data": TrunkMain.objects.all(),
            "logger_data": Logger.objects.all(),
            "hydrant_data": Hydrant.objects.all(),
            "pressure_fitting_data": PressureFitting.objects.all(),
            "pressure_valve_data": PressureControlValve.objects.all(),
            "network_meter_data": NetworkMeter.objects.all(),
            "chamber_data": Chamber.objects.all(),
            "operational_site_data": OperationalSite.objects.all(),
        }
        # 2 includes NetworkOptValve Model
        # model_objects = {
        #     "distribution_mains_data": self.model.objects.all(),
        #     "trunk_mains_data": TrunkMain.objects.all(),
        #     "logger_data": Logger.objects.all(),
        #     "hydrant_data": Hydrant.objects.all(),
        #     "pressure_fitting_data": PressureFitting.objects.all(),
        #     "pressure_valve_data": PressureControlValve.objects.all(),
        #     "network_meter_data": NetworkMeter.objects.all(),
        #     "chamber_data": Chamber.objects.all(),
        #     "operational_site_data": OperationalSite.objects.all(),
        #     "network_opt_valve_data": NetworkOptValve.objects.all(),
        # }
        
        subqueries = {}
        for asset_name, model_object in model_objects.items():
            subqueries[asset_name] = ArraySubquery(self._generate_dwithin_subquery(model_object, json_fields))
        
        return subqueries
        
    def get_pipe_point_relation_queryset(self):
        asset_subqueries = self._generate_asset_subqueries()

        # https://stackoverflow.com/questions/51102389/django-return-array-in-subquery
        qs = self.model.objects.prefetch_related("dmas").annotate(
            asset_name=Value(self.model.AssetMeta.asset_name),
            length=Length("geometry"),
            wkt=AsWKT("geometry"),
            dma_ids=ArrayAgg("dmas"),
            dma_codes=ArrayAgg("dmas__code"),
            dma_names=ArrayAgg("dmas__name"),
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
    
    