from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User, Request


async def create_user(db: AsyncSession, username: str, hashed_password: str) -> User:
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_request(
    db: AsyncSession, user_id: int, text: str, response: str
) -> Request:
    db_request = Request(user_id=user_id, text=text, response=response)
    db.add(db_request)
    await db.commit()
    await db.refresh(db_request)
    return db_request


async def get_all_requests(db: AsyncSession) -> list[Request]:
    result = await db.execute(select(Request))
    return result.scalars().all()
