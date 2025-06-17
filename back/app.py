from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from db.db_connector import db

from routers.user import router as UserRouter
from routers.roadmap import router as RoadmapRouter
from routers.resource import router as ResourceRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.close()

app = FastAPI(
    title="KIZAK",
    summary="API for KIZAK project",
    version="0.0.1",
    lifespan=lifespan
)

app.include_router(UserRouter, tags=['User'])
app.include_router(RoadmapRouter)
app.include_router(ResourceRouter, tags=['Resource'])

if __name__ == "__main__":
    uvicorn.run(app)
