from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from typing import List
from app.schemas import TextRequest, TextResponse
from app.repository import create_request, get_all_requests
from app.auth import get_current_user
from app.auth.models import User

router = APIRouter()

@router.post("/process", response_model=TextResponse)
async def process_text(request: TextRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    response = await create_request(request.text, db, user.id)
    return response

@router.get("/history", response_model=List[TextResponse])
async def get_history(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    requests = await get_all_requests(db, user.id)
    return [{"response": req.response} for req in requests]