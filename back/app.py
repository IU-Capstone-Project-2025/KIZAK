from fastapi import FastAPI
import uvicorn
from pathlib import Path

from routers.user import router as UserRouter
from routers.roadmap import router as RoadmapRouter


app = FastAPI(
    title="KIZAK",
    summary="API for KIZAK project",
    description=Path("back/docs/app.md").read_text(),
    version="0.0.1"
)

app.include_router(UserRouter, tags=['User'])
app.include_router(RoadmapRouter, tags=['Roadmap'])

if __name__ == "__main__":
    uvicorn.run(app)
