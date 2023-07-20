from fastapi import APIRouter, Depends, HTTPException
from config.db import get_db
from models.post import posts
from sqlalchemy.orm import Session
from .auth import AuthHandler
from schemas.post import Post

router = APIRouter(prefix='/api/post', tags=['Post'])