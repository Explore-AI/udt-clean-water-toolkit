from rest_framework.routers import DefaultRouter
from .viewsets import SchematicViewset, SchematicPipeMainViewset

router = DefaultRouter()
router.register(r"schematic", SchematicViewset, basename="schematic")
router.register(
    r"schematic-pipe-main", SchematicPipeMainViewset, basename="schematic-pipe-main"
)

urlpatterns = router.urls
