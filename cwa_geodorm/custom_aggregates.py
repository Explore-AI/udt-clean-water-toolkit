from django.db.models import JSONField
from django.db.models.aggregates import Aggregate


# https://stackoverflow.com/questions/73668842/django-with-mysql-subquery-returns-more-than-1-row
class JSONArrayAgg(Aggregate):
    function = "JSON_ARRAYAGG"
    output_field = JSONField()
