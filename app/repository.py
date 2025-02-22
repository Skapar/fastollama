from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Request
from app.core import settings
from fastapi import HTTPException
import httpx

async def create_request(prompt: str, db: AsyncSession, user_id: int) -> dict:
    payload = {
        "model": "tinyllama",
        "prompt": prompt,
        "stop": ["<|system|>", "<|user|>", "<|assistant|>", "</s>"],
        "stream": False
    }
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(settings.OLLAMA_URL + '/api/generate', json=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Ошибка запроса к Ollama")
        
        data = response.json()
        response_text = data["response"]
        
        db_request = Request(user_id = user_id, text=prompt, response=response_text)
        db.add(db_request)
        await db.commit()
        await db.refresh(db_request)
        
        return {"response": data["response"]}

async def get_all_requests(db: AsyncSession, user_id: int) -> list[Request]:
    result = await db.execute(select(Request).where(Request.user_id == user_id))
    return result.scalars().all()