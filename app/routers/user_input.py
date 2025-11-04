# app/routers/user_input.py
# Endpoint to store user queries (history preserved).

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas
from datetime import datetime

router = APIRouter(prefix="", tags=["user_input"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/user_input")
def post_user_input(payload: schemas.UserInputIn, db: Session = Depends(get_db)):
    """
    Store user query. Frontend provides user_id (from login) and message text.
    Returns created query id and timestamp.
    """
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    row = models.UserQuery(user_id=payload.user_id, query_text=payload.message, created_at=datetime.utcnow())
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"query_id": row.id, "user_id": row.user_id, "created_at": row.created_at.isoformat()}
