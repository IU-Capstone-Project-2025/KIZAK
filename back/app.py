from contextlib import asynccontextmanager

import uvicorn
from db.db_connector import db
from fastapi import FastAPI
from routers.resource import router as ResourceRouter
from routers.roadmap import router as RoadmapRouter
from routers.user import router as UserRouter
from routers.auth import router as AuthRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.close()


app = FastAPI(
    title="KIZAK",
    summary="API for KIZAK project",
    version="0.0.1",
    lifespan=lifespan,
)

app.include_router(UserRouter, tags=["User"])
app.include_router(RoadmapRouter)
app.include_router(ResourceRouter, tags=["Resource"])
app.include_router(AuthRouter, tags=["auth"])



if __name__ == "__main__":
    uvicorn.run(app)
