from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import weather

app = FastAPI(title="Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.router, prefix="/api")
