import uvicorn
from db.db_connector import db

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routers.resource import router as ResourceRouter
from routers.roadmap import router as RoadmapRouter
from routers.user import router as UserRouter
from routers.auth import router as AuthRouter
from routers.utils import router as UtilsRouter
from routers.feedback import router as FeedbackRouter
from routers.mail import router as MailRouter

import dotenv
import os

dotenv.load_dotenv()

os.environ["HF_HOME"] = "/models"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()

    yield
    await db.close()


app = FastAPI(
    title="KIZAK",
    summary="API for KIZAK project",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(UserRouter, tags=["User"])
app.include_router(RoadmapRouter)
app.include_router(ResourceRouter, tags=["Resource"])
app.include_router(AuthRouter, tags=["Auth"])
app.include_router(UtilsRouter, tags=["Utils"])
app.include_router(FeedbackRouter, tags=["Feedback"])
app.include_router(MailRouter, tags=["Mail"])


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("API_HOST"),
                port=int(os.getenv("API_PORT")))
