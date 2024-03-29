from neomodel import IntegerProperty
from .point_node import PointNode
from cwa_geod.core.constants import POINT_ASSET__NAME


class PointAsset(PointNode):
    gid = IntegerProperty(unique_index=True, unique=True, required=True)

    class AssetMeta:
        asset_name = POINT_ASSET__NAME

    @staticmethod
    def get_all_asset_models():
        return PointAsset.__subclasses__()

    @classmethod
    def asset_name_model_mapping(cls, asset_name):
        for model in cls.get_all_asset_models():
            if model.AssetMeta.asset_name == asset_name:
                return model

        return None
