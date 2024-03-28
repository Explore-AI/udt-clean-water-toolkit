from neomodel import IntegerProperty
from .point_node import PointNode


class PointAsset(PointNode):
    gid = IntegerProperty(unique_index=True, unique=True, required=True)

    class AssetMeta:
        asset_name = "point_asset"

    @staticmethod
    def get_all_asset_models():
        return PointAsset.__subclasses__()

    @classmethod
    def asset_name_model_mapping(cls, asset_name):
        for model in cls.get_all_asset_models():
            if model.AssetMeta.asset_name == asset_name:
                return model

        return None
