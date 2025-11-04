# app/database.py
# Database initialization and session factory for SQLite (SQLAlchemy).

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DATABASE_URL = "sqlite:///" + os.path.join(DATA_DIR, "sail.db")

# Engine with check_same_thread False for sqlite + FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for models
Base = declarative_base()


def init_db():
    """Create tables (imports models to register metadata)."""
    # Import models to ensure table metadata is registered
    import app.models as models  # noqa: F401
    Base.metadata.create_all(bind=engine)
