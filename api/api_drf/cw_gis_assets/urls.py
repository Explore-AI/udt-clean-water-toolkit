from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets import (
    TrunkMainViewSet,
    TrunkMainGeoJsonViewSet, 
    DistributionMainViewSet,
    ChamberViewSet,
    HydrantViewSet,
    LoggerViewSet,
    NetworkMeterViewSet,
    NetworkOptValveViewSet,
    OperationalSiteViewSet,
    PressureControlValveViewSet,
    PressureFittingViewSet,
)


router = DefaultRouter()
router.register(r"trunk_main", TrunkMainViewSet, basename="trunk_main")
router.register(r"trunk_main_geojson", TrunkMainGeoJsonViewSet, basename='trunk_main_geojson')
router.register(
    r"distribution_main", DistributionMainViewSet, basename="distribution_main"
)
router.register(r"chamber", ChamberViewSet, basename="chamber")
router.register(r"hydrant", HydrantViewSet, basename="hydrant")
router.register(r"logger", LoggerViewSet, basename="logger")
router.register(r"network_meter", NetworkMeterViewSet, basename="network_meter")
router.register(
    r"network_opt_valve", NetworkOptValveViewSet, basename="network_opt_valve"
)
router.register(
    r"operational_site", OperationalSiteViewSet, basename="operational_site"
)
router.register(
    r"pressure_control_valve",
    PressureControlValveViewSet,
    basename="pressure_control_valve",
)
router.register(
    r"pressure_fitting", PressureFittingViewSet, basename="pressure_fitting"
)

urlpatterns = router.urls
