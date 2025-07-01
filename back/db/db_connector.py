import asyncio
import os
import sys
from contextlib import asynccontextmanager
from typing import Any, Optional

import asyncpg
import dotenv

dotenv.load_dotenv()


class DataBase:
    _pool = None
    def __init__(self):
        
        self._db_config = {
            "user": os.getenv("DB_USER", "user"),
            "password": os.getenv("DB_PASSWORD", "password"),
            "database": os.getenv("DB_NAME", "db"),
            "host": os.getenv("DB_HOST", "db"),
            "port": int(os.getenv("DB_PORT", 5432)),
            "min_size": int(os.getenv("DB_POOL_MIN", 5)),
            "max_size": int(os.getenv("DB_POOL_MAX", 20)),
            "timeout": 30,
        }

    async def connect(self, max_retries: int = 10, delay: float = 1):
        """Wait for the database to be available, then create
        a connection pool"""
        retries = 0
        while retries < max_retries:
            try:
                test_conn = await asyncpg.connect(
                    user=self._db_config["user"],
                    password=self._db_config["password"],
                    database=self._db_config["database"],
                    host=self._db_config["host"],
                    port=self._db_config["port"],
                    timeout=5,
                )
                await test_conn.close()
                print("Database is ready.")
                break
            except Exception as e:
                print(f"Waiting for DB... ({retries+1}/{max_retries}) - {e}")
                await asyncio.sleep(delay)
                retries += 1
        else:
            print("Database did not become available in time. Exiting.")
            sys.exit(1)

        # DB is ready, now initialize the connection pool
        self._pool = await asyncpg.create_pool(**self._db_config)

    async def close(self):
        await self._pool.close()

    @asynccontextmanager
    async def connection(self):
        """Get a connection from the pool with context manager"""
        if not self._pool:
            await self.connect()

        conn = await self._pool.acquire()
        try:
            yield conn
        finally:
            await self._pool.release(conn)

    @asynccontextmanager
    async def transaction(self):
        if not self._pool:
            await self.connect()

        conn = await self._pool.acquire()
        try:
            async with conn.transaction():
                yield conn
        finally:
            await self._pool.release(conn)

    async def fetch(self, query: str, *args) -> list[asyncpg.Record]:
        """Execute a SELECT query and return results"""
        async with self.connection() as conn:
            return await conn.fetch(query, *args)

    async def execute(self, query: str, *args) -> str:
        """Execute an INSERT/UPDATE/DELETE query"""
        async with self.connection() as conn:
            return await conn.execute(query, *args)

    async def executemany(
        self,
        query: str,
        args_seq: list[tuple[Any, ...]] | tuple[tuple[Any, ...], ...],
    ) -> None:
        async with self.connection() as conn:
            await conn.executemany(query, args_seq)

    async def fetchrow(self, query: str, *args) -> Optional[asyncpg.Record]:
        """Execute a SELECT query and return single row"""
        async with self.connection() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args) -> Any:
        """Execute a SELECT query and return single value"""
        async with self.connection() as conn:
            return await conn.fetchval(query, *args)


db = DataBase()
