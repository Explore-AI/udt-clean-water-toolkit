from rest_framework.routers import DefaultRouter
from .viewsets import SchematicViewset

router = DefaultRouter()
router.register(r"schematic", SchematicViewset, basename="schematic")

urlpatterns = router.urls 
