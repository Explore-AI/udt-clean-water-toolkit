import json


class GeoDjangoSerializer:
    """Custom serializers from GeoDjango."""

    srid = 27700  # TODO: set default srid in config

    def queryset_to_geojson(self, qs, srid=None):
        """GeoJSON serialization for properties and geometry
        fields directly queried from the db without modification.
        No iteration."""

        srid = srid or self.srid

        geo_data = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": f"EPSG:{srid}"}},
            "features": list(qs),
        }
        return json.dumps(geo_data)

    def queryset_to_geojson2(self, qs, srid=None):
        """GeoJSON serialization for properties and geometry
        fields."""

        srid = self.srid or srid

        geo_data = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": f"EPSG:{srid}"}},
            "features": [
                {"properties": i["properties"], "geometry": json.loads(i["geometry"])}
                for i in qs
            ],
        }
        return json.dumps(geo_data)
