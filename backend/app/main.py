from fastapi import FastAPI
from app.core.config import settings
from app.api import endpoints
from app.core.database import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    root_path="/manager/api"
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(endpoints.router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to Backup Manager API"}
