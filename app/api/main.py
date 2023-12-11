from typing import Union

from fastapi import FastAPI
from config.settings import APP_TITLE, DEBUG

app = FastAPI(title=APP_TITLE, debug=DEBUG)


@app.get("/")
def read_root():
    return {"Hello": "World"}
