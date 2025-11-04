# app/routers/chatbot.py
# Agent posts textual response; frontend fetches latest response by user_id.

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app import models, schemas

router = APIRouter(prefix="", tags=["chatbot"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/chatbot_response")
def agent_post_response(payload: schemas.AgentResponseIn, db: Session = Depends(get_db)):
    """
    Agent posts a textual response for a user's query.
    If query_id provided, update that query; otherwise update the latest query for the user.
    Agent is unauthenticated (internal).
    """
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    target = None
    if payload.query_id:
        target = db.query(models.UserQuery).filter(models.UserQuery.id == payload.query_id,
                                                   models.UserQuery.user_id == payload.user_id).first()
        if not target:
            raise HTTPException(status_code=404, detail="Query not found for given query_id and user")
    else:
        target = db.query(models.UserQuery).filter(models.UserQuery.user_id == payload.user_id).order_by(
            models.UserQuery.created_at.desc()).first()
        if not target:
            raise HTTPException(status_code=404, detail="No queries found for that user")

    target.response_text = payload.response_text
    target.response_time = datetime.utcnow()
    db.add(target)
    db.commit()
    db.refresh(target)
    return {"status": "success", "query_id": target.id, "user_id": payload.user_id}


@router.get("/chatbot_response")
def get_latest_response(user_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Frontend fetches latest query and its response_text for provided user_id.
    Returns only text fields (JSON).
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    latest = db.query(models.UserQuery).filter(models.UserQuery.user_id == user_id).order_by(
        models.UserQuery.created_at.desc()).first()
    if not latest:
        return {"query_id": None, "query_text": None, "response_text": None, "response_time": None}

    return {
        "query_id": latest.id,
        "query_text": latest.query_text,
        "response_text": latest.response_text,
        "response_time": latest.response_time.isoformat() if latest.response_time else None,
        "created_at": latest.created_at.isoformat()
    }
