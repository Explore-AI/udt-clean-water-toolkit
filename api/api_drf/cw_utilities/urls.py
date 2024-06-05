from rest_framework.routers import DefaultRouter
from .viewsets import DmaViewSet

router = DefaultRouter()
router.register(r"dma", DmaViewSet, basename="dma")

urlpatterns = router.urls
