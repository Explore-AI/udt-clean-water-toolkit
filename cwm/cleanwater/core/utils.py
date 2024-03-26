from django.contrib.gis.geos import Point


def normalised_point_position_on_line(
    line_geom, start_of_line_point, point_geom, srid=None
):
    """Get the normalised position of a Point geometry on a LineString geometry relative to the
    LineString start Point.

    Params:
           line_geom, LineString geometry, required
           start_of_line_point, Point geometry, required
           point_geom, Point geometry, required
           srid, int, optional

    Returns:
           normalised_position_on_line, float

    """

    # https://zach.se/geodesic-distance-between-points-in-geodjango/
    # https://docs.djangoproject.com/en/5.0/ref/contrib/gis/geos/
    normalised_position_on_line = 1 - (
        (line_geom.length - start_of_line_point.distance(point_geom)) / line_geom.length
    )

    return normalised_position_on_line
