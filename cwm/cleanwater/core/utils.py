from django.contrib.gis.geos import Point


def normalised_point_position_on_line(line_geom, point_geom, srid=None):
    """Get the normalised position of a Point on a Line relative to the
    Line start Point. The Line start Point is the first set of coordinates
    in the tuple returned by geometry.coords where geometry is a
    LineString or MultiLineString"""

    start_of_line_point = Point(line_geom.coords[0][0], srid=srid)

    # https://zach.se/geodesic-distance-between-points-in-geodjango/
    # TODO: fix below distane calc as not geodesic
    # https://docs.djangoproject.com/en/5.0/ref/contrib/gis/geos/
    normalised_position_on_line = 1 - (
        (line_geom.length - start_of_line_point.distance(point_geom)) / line_geom.length
    )

    return normalised_position_on_line
