from fastapi import FastAPI
from config.settings import APP_TITLE, DEBUG
from core.routers import RouterUtils
from core.urls import url_routes


app = FastAPI(title=APP_TITLE, debug=DEBUG)


RouterUtils.generate_routers(app, url_routes)


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
