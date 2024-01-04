from cleanwater.controllers.network_controller import NetworkController
from cwa_geod.assets.controllers import TrunkMainsController
from cwa_geod.config.settings import DEFAULT_SRID


class GisToGraphNetwork(NetworkController):
    """Create a graph network of assets from a geospatial
    network of assets"""

    def __init__(self, srid=None):
        self.srid = srid or DEFAULT_SRID
        super().__init__(self.srid)

    def create_network(self):
        return self._create_trunk_mains_graph()

    def _create_trunk_mains_graph(self):
        tm = TrunkMainsController()
        trunk_mains = tm.get_geometry_queryset()
        return self.create_pipes_network(trunk_mains)
