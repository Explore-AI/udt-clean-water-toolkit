from fastapi import FastAPI
from config.settings import APP_TITLE, DEBUG
from config.routers import RouterUtils

from config.urls import url_routes


app = FastAPI(title=APP_TITLE, debug=DEBUG)


RouterUtils.generate_routers(app, url_routes)


# @app.get("/items/")
# async def read_items():
#     return [{"name": "Katana"}]


# from pydantic import BaseModel


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# @app.post("/items/")
# async def create_item(item: Item):
#     return item


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
