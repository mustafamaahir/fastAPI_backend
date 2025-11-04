# app/schemas.py
# Pydantic schemas for request/response validation.

from pydantic import BaseModel
from typing import List, Optional


class SignupIn(BaseModel):
    username: str
    password: str


class LoginIn(BaseModel):
    username: str
    password: str


class UserInputIn(BaseModel):
    user_id: int
    message: str


class AgentResponseIn(BaseModel):
    user_id: int
    response_text: str
    query_id: Optional[int] = None


class ForecastItem(BaseModel):
    date: str  # "YYYY-MM-DD"
    rainfall: float


class ForecastList(BaseModel):
    __root__: List[ForecastItem]
