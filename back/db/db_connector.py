import asyncpg
import dotenv
import os

dotenv.load_dotenv()

db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "db": os.getenv("DB_NAME"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

async def get_conn():
    return await asyncpg.connect(**db_config)
