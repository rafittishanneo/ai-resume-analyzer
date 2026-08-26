from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.controllers.resume_controller import router


app = FastAPI(
    title="AI Resume Analyzer",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "views" / "static"),
    name="static",
)

app.include_router(router)