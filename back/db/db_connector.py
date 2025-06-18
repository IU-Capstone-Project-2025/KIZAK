import os
from contextlib import asynccontextmanager
from typing import Any, Optional

import asyncpg
import dotenv

dotenv.load_dotenv()


class DataBase:
    def __init__(self):
        self._pool = None
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

    async def connect(self):
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
