from pathlib import Path
from fastapi.security import OAuth2PasswordBearer

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


APP_TITLE = "UDT"

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


MODELS = ["aerich.models", "core.models"]


DATABASES = {
    "default": {
        "ENGINE": "sqlite://",
        "NAME": "db.sqlite3",
    }
}

DB_URL = f"{DATABASES['default']['ENGINE']}{DATABASES['default']['NAME']}"

TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": MODELS,
            "default_connection": "default",
        }
    },
}


OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")


DEBUG = True
