from neomodel import db, install_labels, remove_all_labels
from .trunk_main import TrunkMain
from .distribution_main import DistributionMain
from .hydrant import Hydrant
from .chamber import Chamber
from .logger import Logger
from .network_meter import NetworkMeter
from .network_opt_valve import NetworkOptValve
from .operational_site import OperationalSite
from .pressure_control_valve import PressureControlValve
from .pressure_fitting import PressureFitting
from .pipe_end import PipeEnd
from .point_asset import PointAsset


def initialise_node_labels():
    """Setup constraints based on network models"""

    # Can't find count function in nodel model so using cypher query
    # Note: do not use __len__ as it's very slow for large number of nodes
    node_count = db.cypher_query("match (n) return count (n);")[0][0][0]

    if node_count == 0:
        remove_all_labels()
        install_labels(PipeEnd)  # quiet=True
