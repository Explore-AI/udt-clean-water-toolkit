from neomodel import db, install_labels, remove_all_labels
from .pipe_end import PipeEnd
from .point_asset import PointAsset
from .pipe_main import PipeMain
from .has_dma import HasDma
from .has_utility import HasUtility
from .network_node import NetworkNode
from .pipe_junction import PipeJunction
from .dma import DMA
from .utility import Utility


def initialise_node_labels():
    """Setup constraints based on network models"""

    # Can't find count function in nodel model so using cypher query
    # Note: do not use __len__ as it's very slow for large number of nodes
    node_count = db.cypher_query("match (n) return count (n);")[0][0][0]

    if node_count == 0:
        remove_all_labels()
        install_labels(NetworkNode, quiet=False)
        install_labels(DMA, quiet=False)
        install_labels(Utility, quiet=False)
        install_labels(PipeMain, quiet=False)
        install_labels(HasDma, quiet=False)
        install_labels(HasUtility, quiet=False)
