from fastapi import FastAPI
from config.settings import APP_TITLE, DEBUG
from config.routers import RouterUtils
from config.urls import url_routes


app = FastAPI(title=APP_TITLE, debug=DEBUG)


RouterUtils.generate_routers(app, url_routes)


@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
