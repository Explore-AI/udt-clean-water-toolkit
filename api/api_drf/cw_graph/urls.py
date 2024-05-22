from rest_framework.routers import DefaultRouter
from .viewsets import Neo4jViewset

router = DefaultRouter()
router.register(r"neo4j", Neo4jViewset, basename="neo4j")

urlpatterns = router.urls 
