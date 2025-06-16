import asyncpg

async def get_db_connection():
    conn = await asyncpg.connect(host='localhost:5432',
                            database='db',
                            user='user',
                            password='password')
    return conn
