from rest_framework.routers import DefaultRouter
from .viewsets import SpatialGraphViewset, SchematicPipeMainViewset, SchematicViewset

router = DefaultRouter()
router.register(r"spatial_graph", SchematicViewset, basename="spatial_graph")
router.register(
    r"schematic_pipe_main", SchematicPipeMainViewset, basename="schematic_pipe_main"
)

urlpatterns = router.urls
