from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_db


async def get_session(session: AsyncSession = Depends(get_db)) -> AsyncSession:
    """Dependency for getting database session."""
    return session