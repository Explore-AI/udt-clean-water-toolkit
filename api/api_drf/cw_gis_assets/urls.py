from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter, Route, DynamicRoute
from .viewsets import (
    PipeMainViewSet,
    PipeMainGeoJsonViewSet,
    # DistributionMainViewSet,
    # DistributionMainGeoJsonViewSet,
    ChamberViewSet,
    ChamberGeoJsonViewSet,
    HydrantViewSet,
    HydrantGeoJsonViewSet,
    LoggerViewSet,
    LoggerGeoJsonViewSet,
    NetworkMeterViewSet,
    NetworkMeterGeoJsonViewSet,
    NetworkOptValveViewSet,
    NetworkOptValveGeoJsonViewSet,
    OperationalSiteViewSet,
    OperationalSiteGeoJsonViewSet,
    PressureControlValveViewSet,
    PressureControlValveGeoJsonViewSet,
    PressureFittingViewSet,
    PressureFittingGeoJsonViewSet,
    PipeFlowViewSet,
)


router = DefaultRouter()

router.register(r"pipe_main", PipeMainViewSet, basename="pipe_main")
router.register(r"geojson/pipe_main", PipeMainGeoJsonViewSet, "pipe_main-geojson")
router.register(r"chamber", ChamberViewSet, basename="chamber")
router.register(r"geojson/chamber", ChamberGeoJsonViewSet, "chamber-geojson")
router.register(r"hydrant", HydrantViewSet, basename="hydrant")
router.register(r"geojson/hydrant", HydrantGeoJsonViewSet, "hydrant-geojson")
router.register(r"logger", LoggerViewSet, basename="logger")
router.register(r"geojson/logger", LoggerGeoJsonViewSet, "logger-geojson")
router.register(r"network_meter", NetworkMeterViewSet, basename="network_meter")
router.register(
    r"geojson/network_meter", NetworkMeterGeoJsonViewSet, "network_meter-geojson"
)
router.register(
    r"network_opt_valve", NetworkOptValveViewSet, basename="network_opt_valve"
)
router.register(
    r"geojson/network_opt_valve",
    NetworkOptValveGeoJsonViewSet,
    "network_opt_valve-geojson",
)
router.register(
    r"operational_site", OperationalSiteViewSet, basename="operational_site"
)
router.register(
    r"geojson/operational_site",
    OperationalSiteGeoJsonViewSet,
    "operational_site-geojson",
)
router.register(
    r"pressure_control_valve",
    PressureControlValveViewSet,
    basename="pressure_control_valve",
)
router.register(
    r"geojson/pressure_control_valve",
    PressureControlValveGeoJsonViewSet,
    "pressure_control_valve-geojson",
)
router.register(
    r"pressure_fitting", PressureFittingViewSet, basename="pressure_fitting"
)
router.register(
    r"geojson/pressure_fitting",
    PressureFittingGeoJsonViewSet,
    "pressure_fitting-geojson",
)

router.register(r"pipe_flows", PipeFlowViewSet, basename="pipe_flows")

urlpatterns = router.urls
