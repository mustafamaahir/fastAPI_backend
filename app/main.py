# app/main.py
# FastAPI app entrypoint. Initializes PostgreSQL DB and mounts routers.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db, SessionLocal
from app import models  # ✅ make sure models are imported before init_db()
from app.routers import auth, user_input, chatbot, forecast
from datetime import datetime
import json

app = FastAPI(
    title="Rainfall Project SAIL - Forecast API",
    version="1.0.0",
    description="Backend for rainfall forecasts, user queries, and agent-posted data."
)

# ---- Initialize database ----
init_db()

# ---- CORS ----
origins = [
    "http://localhost",
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ---- Routers ----
app.include_router(auth.router)
app.include_router(user_input.router)
app.include_router(chatbot.router)
app.include_router(forecast.router)

# ---- Seed dummy data ----
@app.on_event("startup")
def seed_dummy_data():
    db = SessionLocal()
    try:
        if not db.query(models.Forecast).first():
            print("🌱 Inserting dummy forecast data...")
            dummy_daily = [
                {"date": "2021-10-10", "rainfall": 14},
                {"date": "2021-10-11", "rainfall": 7},
                {"date": "2021-10-12", "rainfall": 20},
                {"date": "2021-10-13", "rainfall": 12},
                {"date": "2021-10-14", "rainfall": 9},
                {"date": "2021-10-15", "rainfall": 18},
                {"date": "2021-10-16", "rainfall": 6}
            ]
            dummy_monthly = [
                {"date": "2021-10-10", "rainfall": 14},
                {"date": "2021-11-11", "rainfall": 7},
                {"date": "2021-12-12", "rainfall": 20}
            ]
            db.add_all([
                models.Forecast(
                    forecast_type="daily",
                    forecast_data=json.dumps(dummy_daily),
                    created_at=datetime.utcnow(),
                ),
                models.Forecast(
                    forecast_type="monthly",
                    forecast_data=json.dumps(dummy_monthly),
                    created_at=datetime.utcnow(),
                ),
            ])
            db.commit()
            print("✅ Dummy forecast data inserted successfully.")
        else:
            print("✅ Forecast data already exists — skipping dummy insert.")
    finally:
        db.close()

@app.api_route("/status", methods=["GET", "HEAD"])
def status():
    return {"status": "ok", "message": "Rainfall Project SAIL API is running."}
