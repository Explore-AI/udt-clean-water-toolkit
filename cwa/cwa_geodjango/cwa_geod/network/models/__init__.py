from neomodel import db, install_labels, remove_all_labels
from .pipe_end import PipeEnd
from .point_asset import PointAsset
from .pipe_relation import PipeRelation
from .point_node import PointNode
from .pipe_junction import PipeJunction


def initialise_node_labels():
    """Setup constraints based on network models"""

    # Can't find count function in nodel model so using cypher query
    # Note: do not use __len__ as it's very slow for large number of nodes
    node_count = db.cypher_query("match (n) return count (n);")[0][0][0]

    if node_count == 0:
        remove_all_labels()
        install_labels(PipeEnd, quiet=True)
        install_labels(PipeRelation, quiet=True)
        install_labels(PipeJunction, quiet=True)
        install_labels(PointAsset, quiet=True)
