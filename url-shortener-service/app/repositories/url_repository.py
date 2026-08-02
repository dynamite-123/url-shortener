from uuid import UUID
from datetime import datetime

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.url import URL


class URLRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create(self, url: URL) -> URL:
        self.db.add(url)
        await self.db.commit()
        await self.db.refresh(url)
        return url

    # Read operations
    async def get_by_id(self, id: int) -> URL | None:
        result = await self.db.execute(select(URL).where(URL.id == id))
        return result.scalar_one_or_none()

    async def get_by_short_code(self, short_code: str) -> URL | None:
        result = await self.db.execute(select(URL).where(URL.short_code == short_code))
        return result.scalar_one_or_none()

    async def get_by_original_url(
        self,
        original_url: str,
        owner_id: UUID | None = None,
    ) -> URL | None:
        query = select(URL).where(URL.original_url == original_url)

        if owner_id is not None:
            query = query.where(URL.owner_id == owner_id)

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    # Update operations
    async def increment_click_count(self, id: int) -> None:
        await self.db.execute(
            update(URL).where(URL.id == id).values(click_count=URL.click_count + 1)
        )
        await self.db.commit()

    async def update_expiration(
        self,
        id: int,
        expires_at: datetime | None,
    ) -> None:
        await self.db.execute(
            update(URL).where(URL.id == id).values(expires_at=expires_at)
        )
        await self.db.commit()

    async def activate(self, id: int) -> None:
        await self.db.execute(update(URL).where(URL.id == id).values(is_active=True))
        await self.db.commit()

    async def deactivate(self, id: int) -> None:
        await self.db.execute(update(URL).where(URL.id == id).values(is_active=False))
        await self.db.commit()

    # Delete
    async def delete(self, id: int) -> None:
        await self.db.execute(delete(URL).where(URL.id == id))
        await self.db.commit()
