from rest_framework.routers import DefaultRouter
from .viewsets import SchematicViewset, SchematicTrunkMainViewset

router = DefaultRouter()
router.register(r"schematic", SchematicViewset, basename="schematic")
router.register(r"schematic-trunk-main", SchematicTrunkMainViewset, basename="schematic-trunk-main")

urlpatterns = router.urls 
