from core.urls import router as core_router
from config.auth.backends import login_for_access_token

url_routes = [("/core", core_router)]
