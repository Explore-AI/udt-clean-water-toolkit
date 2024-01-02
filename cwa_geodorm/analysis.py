import setup  # Required. Do not remove.
from django.core.serializers import serialize
from cwa_geod.assets.serializers import TrunkMainGeoJsonSerializer
from cwa_geod.assets.models import Logger
from cwa_geod.config.settings import DEFAULT_SRID


# https://docs.djangoproject.com/en/5.0/ref/contrib/gis/db-api/#spatial-lookups
# https://docs.djangoproject.com/en/5.0/ref/contrib/gis/geoquerysets/#std-fieldlookup-dwithin


# NOTE: The crux of the below two examples is that one can contruct a graph from
# lines or points using geojson. Need to figure out how to create graph that has
# both lines and points as geojson can combine only one layer. Can we create a layer that has
# both lines and points and then convert it to geojson


# https://networkx.org/documentation/stable/auto_examples/geospatial/plot_lines.html
# https://docs.momepy.org/en/stable/user_guide/graph/convert.html # alternate


# TrunkMain.objects.all().select_related("dma").prefetch_related("dma__dma_loggers")
# from django.contrib.gis.measure import D
# TrunkMain.objects.filter(geometry=(geom, D(m=5)))
# https://stackoverflow.com/a/65324191
# https://postgis.net/docs/ST_ClosestPoint.html
# https://docs.djangoproject.com/en/5.0/ref/contrib/gis/functions/#django.contrib.gis.db.models.functions.ClosestPoint


# tgeo = TrunkMain.objects.first().geometry
# Logger.objects.annotate(dist=Distance(tgeo, "geometry")).all().order_by("dist").first().dist

import json


def _geojson_serialize_feature_collection_redux(qs):
    geo_data = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": f"EPSG:{DEFAULT_SRID}"}},
        "features": list(qs)
        # "features": [
        #     {"properties": i["properties"], "geometry": json.loads(i["geometry"])}
        #     for i in qs
        # ],
    }
    return json.dumps(geo_data)


def _geojson_serialize_feature_collection(qs):
    # see https://postgis.net/docs/ST_AsGeoJSON.html
    geo_data = {
        "type": "FeatureCollection",
        "crs": {"type": "name", "properties": {"name": f"EPSG:{DEFAULT_SRID}"}},
        "features": [
            {"properties": i["properties"], "geometry": json.loads(i["geometry"])}
            for i in qs
        ],
    }
    return json.dumps(geo_data)


def graph_from_trunk_mains():
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import momepy
    import networkx as nx

    serializer = TrunkMainGeoJsonSerializer()
    trunk_mains_data = serializer.tw_trunk_mains_to_geojson()
    import pdb

    pdb.set_trace()
    trunk_mains_gdf = gpd.read_file(trunk_mains_data)
    trunk_mains_as_single_lines_gdf = trunk_mains_gdf.explode(index_parts=True)
    G = momepy.gdf_to_nx(trunk_mains_as_single_lines_gdf, approach="primal")

    positions = {n: [n[0], n[1]] for n in list(G.nodes)}

    f, ax = plt.subplots(1, 2, figsize=(12, 6), sharex=True, sharey=True)
    trunk_mains_gdf.plot(color="k", ax=ax[0])
    for i, facet in enumerate(ax):
        facet.set_title(("TrunkMains Geospatial", "TrunkMains Graph")[i])
        facet.axis("off")

    nx.draw(G, positions, ax=ax[1], node_size=5)

    plt.show()


# https://networkx.org/documentation/stable/auto_examples/geospatial/plot_lines.html
# Lots of island loggers as expected
def graph_from_loggers():
    from libpysal import weights
    from contextily import add_basemap
    import numpy as np

    logger_data = serialize(
        "geojson", Logger.objects.all(), geometry_field="geometry", srid=DEFAULT_SRID
    )

    logger_gdf = gpd.read_file(logger_data)

    coordinates = np.column_stack((logger_gdf.geometry.x, logger_gdf.geometry.y))

    knn3 = weights.KNN.from_dataframe(logger_gdf, k=3)

    dist = weights.DistanceBand.from_array(coordinates, threshold=50)

    knn_graph = knn3.to_networkx()
    dist_graph = dist.to_networkx()

    positions = dict(zip(knn_graph.nodes, coordinates))

    f, ax = plt.subplots(1, 2, figsize=(8, 4))
    for i, facet in enumerate(ax):
        logger_gdf.plot(marker=".", color="orangered", ax=facet)
        add_basemap(facet)
        facet.set_title(("KNN-3", "50-meter Distance Band")[i])
        facet.axis("off")
    nx.draw(knn_graph, positions, ax=ax[0], node_size=5, node_color="b")
    nx.draw(dist_graph, positions, ax=ax[1], node_size=5, node_color="b")
    plt.show()


def analysis():
    graph_from_trunk_mains()
    # graph_from_loggers()


analysis()
