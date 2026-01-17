import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GRID_GRAPHQL_URL = os.getenv("GRID_GRAPHQL_URL")
    GRID_API_KEY = os.getenv("GRID_API_KEY")

    REDIS_URL = os.getenv("REDIS_URL")
    POSTGRES_DSN = os.getenv("POSTGRES_DSN")

    REQUEST_TIMEOUT = 20
