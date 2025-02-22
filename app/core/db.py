from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.models import Base

class MongoDB:
    client: AsyncIOMotorClient = None

mongodb = MongoDB()

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=settings.POSTGRES_ECHO,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(settings.MONGO_URL)
    print("Connected to MongoDB")

async def close_mongo_connection():
    mongodb.client.close()
    print("Closed MongoDB connection")
