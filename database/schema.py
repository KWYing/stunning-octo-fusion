"""Module Schema for Model"""
from typing import List
from datetime import datetime
from pydantic import BaseModel


class Info(BaseModel):
    """Info Base Model"""
    sku: str
    title: str
    actress: List[str]
    studio: str
    release_date: datetime
    cover_image: str
    create_at: datetime


class InfoResponse(Info):
    """Info Response Model"""
    id: str


class Actress(BaseModel):
    """Actress Base Model"""
    name: str
    videos: List[str]

class ActressResponse(Actress):
    """Actress Response"""
    id: str
