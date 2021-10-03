import os
from dotenv import load_dotenv

load_dotenv(os.environ.get("DOTENV", ".env"))


SECRET_KEY = os.getenv("SECRET_KEY")
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
ACCESS_TOKEN_EXPIRE_DAYS = os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgres://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_IP}:{DATABASE_PORT}/{DATABASE_NAME}".format(
        **os.environ
    ),
)
