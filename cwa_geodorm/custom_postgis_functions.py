from django.db.models import JSONField
from django.contrib.gis.db.models import LineStringField
from django.db.models.aggregates import Aggregate
from django.contrib.gis.db.models.functions import GeoFunc


# https://stackoverflow.com/questions/73668842/django-with-mysql-subquery-returns-more-than-1-row
class JSONArrayAgg(Aggregate):
    function = "JSON_ARRAYAGG"
    output_field = JSONField()


# https://stackoverflow.com/questions/47471324/divide-multipolygon-area-into-subarea
class SplitGeom(GeoFunc):
    function = "ST_Split"


class DumpGeom(GeoFunc):
    function = "ST_Dump"
    output_field = LineStringField()


# https://stackoverflow.com/questions/56441062/how-to-use-st-line-locate-point-with-a-multilinestring-convertion-in-postgis
class LineMerge(GeoFunc):
    function = "ST_LineMerge"
