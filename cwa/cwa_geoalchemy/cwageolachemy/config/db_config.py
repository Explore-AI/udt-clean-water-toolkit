from sqlalchemy import create_engine
from .config_manager import Settings as AppSettings 

app_settings = AppSettings()
HOST = app_settings.POSTGIS_DEFAULT_DB_HOST
NAME = app_settings.POSTGIS_DB_NAME
USER = app_settings.POSTGIS_DB_USER
PASSWORD = app_settings.POSTGIS_DEFAULT_DB_PASSWORD


engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}/{NAME}")