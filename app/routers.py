from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.db import get_db
from app.models import User, Request
from passlib.context import CryptContext
from typing import List
from app.schemas import TextRequest, TextResponse, UserCreate

router = APIRouter()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@router.post("/api/register", response_model=dict)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"message": "User created successfully"}


@router.post("/api/process", response_model=TextResponse)
async def process_text(request: TextRequest, db: AsyncSession = Depends(get_db)):
    response_text = "Обработанный текст"
    db_request = Request(user_id=1, text=request.text, response=response_text)
    db.add(db_request)
    await db.commit()
    await db.refresh(db_request)
    return {"response": response_text}


@router.get("/api/history", response_model=List[TextResponse])
async def get_history(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Request))
    requests = result.scalars().all()
    return [{"response": req.response} for req in requests]
