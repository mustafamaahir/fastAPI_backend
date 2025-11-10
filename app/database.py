# app/database.py
# Database initialization and session factory for PostgreSQL (Render) or SQLite (local fallback).

import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
import app as models

# ---- Environment Variable ----
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL is not set! Please add it in Render environment settings.")

# Render provides URLs like "postgres://", but SQLAlchemy expects "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# ---- Engine Setup ----
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Change to True if you want SQL logs
)

# ---- Session Setup ----
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# ---- Base Class for Models ----
Base = declarative_base()

def get_db():
    """Yields a new SQLAlchemy database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initializes or rebuilds database tables (for Render PostgreSQL)."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if "users" in tables:
        columns = [col["name"] for col in inspector.get_columns("users")]
        if "email" not in columns:
            print("⚠️ Outdated schema detected — rebuilding database...")
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)
            print("✅ Database successfully rebuilt with latest schema.")
            return

    Base.metadata.create_all(bind=engine)
    print("✅ PostgreSQL database initialized successfully.")
