from sqlalchemy import Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    text = Column(String)
    response = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
