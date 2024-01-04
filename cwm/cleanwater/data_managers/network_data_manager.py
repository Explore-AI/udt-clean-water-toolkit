from momepy import gdf_to_nx
from . import BaseDataManager, GeoDjangoDataManager


# TO DO: fixing inheritence in data managers
class NetworkDataManager(GeoDjangoDataManager):
    def gdf_lines_to_nx_graph(self, geodataframe, method="momepy"):
        """Convert a geopandas dataframe with lines or multilines
        only to a networkx graph"""
        if method == "momepy":
            return self.momepy_gdf_lines_to_graph(geodataframe)
        elif method == "abinitio":
            pass

    def momepy_gdf_lines_to_graph(self, geodataframe):
        """Convert a geopandas dataframe with lines or multilines
        only to a networkx graph using the momepy gdf_to_nx method"""
        gdf = geodataframe.explode(index_parts=True)
        return gdf_to_nx(gdf, approach="primal")
