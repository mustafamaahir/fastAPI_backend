# app/database.py
# Database initialization and session factory for PostgreSQL (Render) or SQLite (local fallback).

import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base

# ---- Path Setup ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ---- Database URL Selection ----
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback to local SQLite during local dev
if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'sail.db')}"
    connect_args = {"check_same_thread": False}
else:
    # Convert Render’s postgres:// URL → postgresql:// (SQLAlchemy format)
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    connect_args = {}

# ---- Engine Setup ----
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)

# ---- Session Setup ----
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# ---- Base Class ----
Base = declarative_base()

def get_db():
    """Provide a new SQLAlchemy database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create all database tables in PostgreSQL or SQLite."""
    from app import models  # ✅ ensure models are imported here

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if not tables:
        print("⚙️ No tables detected — creating all tables in database...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables successfully created in database.")
    else:
        print(f"✅ Existing tables detected: {tables}")
