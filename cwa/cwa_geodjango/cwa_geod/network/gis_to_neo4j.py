from django.contrib.gis.geos import Point
from django.db.models.query import QuerySet
from . import GisToGraph
from cwa_geod.core.constants import DEFAULT_SRID


class GisToNeo4J(GisToGraph):
    """Create a Neo4J graph of assets from a geospatial
    network of assets"""

    def __init__(self, srid: int):
        self.srid: int = srid or DEFAULT_SRID
        super().__init__(self.srid)
