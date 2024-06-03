from neomodel import db, install_labels, remove_all_labels
from .point_asset import PointAsset
from .pipe_end import PipeEnd
from .pipe_relation import PipeRelation
from .network_node import NetworkNode
from .pipe_junction import PipeJunction


def initialise_node_labels(): 
    """ setup constraints based on network models """
    
    node_count = db.cypher_query("match (n) return count (n);")[0][0][0]
    
    if node_count == 0:
        remove_all_labels()
        install_labels(PointAsset, quiet=True)
        install_labels(PipeEnd, quiet=True)
        install_labels(PipeRelation, quiet=True)
        install_labels(NetworkNode, quiet=True)
        install_labels(PipeJunction, quiet=True)
