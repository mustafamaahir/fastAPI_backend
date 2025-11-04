# app/main.py
# Application entrypoint. Mounts routers and initializes DB.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routers import auth, user_input, chatbot, forecast

app = FastAPI(title="Rainfall Project SAIL - Forecast API", version="1.0.0",
              description="Backend for user queries, agent-posted forecasts, and PNG charts for frontend.")

# initialize database and tables
init_db()

# CORS (development)
origins = [
    "http://localhost",
    "http://localhost:8501",
    "http://127.0.0.1:8501",
    "*"  # development only; restrict in production
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])

# include routers
app.include_router(auth.router)
app.include_router(user_input.router)
app.include_router(chatbot.router)
app.include_router(forecast.router)


@app.get("/status")
def status():
    """
    Health check endpoint.
    """
    return {"status": "ok", "message": "Rainfall Project SAIL API is running."}
