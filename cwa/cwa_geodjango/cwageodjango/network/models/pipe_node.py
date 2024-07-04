from neomodel import Relationship
from .network_asset import NetworkAsset
from .pipe_main import PipeMain
from .has_asset import HasAsset


class PipeNode(NetworkAsset):
    pipe_main = Relationship("PipeMain", "PIPE_MAIN", model=PipeMain)
    has_asset = Relationship("HasAsset", "HAS_ASSET", model=HasAsset)
