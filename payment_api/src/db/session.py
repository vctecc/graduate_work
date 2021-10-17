from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from src.core.config import settings


engine = create_async_engine(settings.database.sqlalchemy_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db() -> Session:
    async with async_session() as session:
        async with session.begin():
            try:
                return session
            finally:
                await session.close()