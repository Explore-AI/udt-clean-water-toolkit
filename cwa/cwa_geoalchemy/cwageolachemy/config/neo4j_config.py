from .config_manager import Settings as AppSettings 
from neomodel import config

app_settings = AppSettings()

NEO4J_HOST = app_settings.NEO4J_HOST
NEO4J_USER = app_settings.NEO4J_USER
NEO4J_PWD = app_settings.NEO4J_PASSWORD
NEO4J_PORT = app_settings.NEO4J_PORT


DATABASE_URL = f"bolt://{NEO4J_USER}:{NEO4J_PWD}@{NEO4J_HOST}:{NEO4J_PORT}"
config.DATABASE_URL = DATABASE_URL
