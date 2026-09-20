from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import datetime
import os
from dotenv import load_dotenv

from app.routers import forecast, surplus, match, route, dashboard, anumaan

load_dotenv()

app = FastAPI(title="Food Waste Reduction API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(forecast.router)
app.include_router(surplus.router)
app.include_router(match.router)
app.include_router(route.router)
app.include_router(dashboard.router)
app.include_router(anumaan.router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}
