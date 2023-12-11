from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from config.settings import APP_TITLE, DB_URL, MODELS, DEBUG, CONFIG

app = FastAPI(title=APP_TITLE, debug=DEBUG)


@app.get("/")
def read_root():
    return {"Hello": "World"}


register_tortoise(
    app,
    config=CONFIG,
    db_url=DB_URL,
    modules={"models": MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)
