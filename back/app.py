import uvicorn
from db.db_connector import db
from utils.logger import logger

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

from services.course_scrapper import Scraper

import dotenv
import os
import asyncio

dotenv.load_dotenv()

async def periodic_scrape():
    scraper = Scraper()
    logger.info("Starting to scrape")
    await asyncio.sleep(60) 
    while True:
        try:
            await scraper.scrape_courses()
            await scraper.add_to_db()
            logger.info("Scraping completed successfully. Waiting for next run...")
        except Exception as e:
            logger.error(f"Error in periodic scrape: {e}")
        await asyncio.sleep(24 * 60 * 60) 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    asyncio.create_task(periodic_scrape())
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
