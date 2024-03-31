from django.contrib.gis.geos import Point


def normalised_point_position_on_line(line_geom, start_of_line_point, point_geom):
    """Get the normalised position of a Point geometry on a LineString geometry relative to the
    LineString start Point.

    https://zach.se/geodesic-distance-between-points-in-geodjango/
    https://docs.djangoproject.com/en/5.0/ref/contrib/gis/geos/

    Params:
           line_geom (LineString geometry, required)
           start_of_line_point (Point geometry, required)
           point_geom (Point geometry, required)

    Returns:
           normalised_position_on_line (float)
           distance_from_line_start (float)
    """

    distance_from_line_start = start_of_line_point.distance(point_geom)

    # TODO: fix exception message
    if type(distance_from_line_start) not in (int, float):
        raise Exception("The calculated distance must be an int or float.")

    normalised_position_on_line = 1 - (
        (line_geom.length - distance_from_line_start) / line_geom.length
    )

    return normalised_position_on_line, distance_from_line_start
