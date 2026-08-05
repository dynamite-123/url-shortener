from app.repositories.url_repository import URLRepository
from app.schemas.url import CreateURLRequest
from app.schemas.auth import User
from redis.asyncio import Redis
from app.models.url import URL
from app.services.short_url import create_short_code
from datetime import datetime, timezone


from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

class URLService:
    def __init__(self, repo: URLRepository, redis: Redis):
        self.repo = repo
        self.redis = redis

    async def create_url(
        self,
        create_url_request: CreateURLRequest,
        user: User,
    ) -> URL:
        """Create a new shortened URL for the given user."""
        counter, short_code = await create_short_code(self.redis)
        print("###########################")
        print(short_code)

        url = URL(
            id=counter,
            short_code=short_code,
            original_url=str(create_url_request.original_url),
            owner_id=user.id,
            expires_at=create_url_request.expires_at,
        )

        try:
            return await self.repo.create(url)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to create short URL. Please try again.",
            )

    async def delete_url(self, url_id: int, user: User) -> None:
        """Delete a shortened URL if the user is the owner."""
        url = await self.repo.get_by_id(url_id)

        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL not found",
            )

        if url.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this URL",
            )

        await self.repo.delete(url.id)

    async def deactivate_url(self, url_id: int, user: User) -> None:
        """Deactivate a shortened URL if the user is the owner."""
        url = await self.repo.get_by_id(url_id)

        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL not found",
            )

        if url.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to deactivate this URL",
            )

        await self.repo.deactivate(url.id)

    async def activate_url(self, url_id: int, user: User) -> None:
        """Activate a shortened URL if the user is the owner."""
        url = await self.repo.get_by_id(url_id)

        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL not found",
            )

        if url.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to activate this URL",
            )

        await self.repo.activate(url.id)

    async def update_expiration(self, url_id: int, expires_at: str | None, user: User) -> None:
        """Update the expiration date of a shortened URL if the user is the owner."""
        url = await self.repo.get_by_id(url_id)

        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL not found",
            )

        if url.owner_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this URL",
            )

        await self.repo.update_expiration(url.id, expires_at)

    async def get_url_by_id(self, url_id: int) -> URL | None:
        """Retrieve a shortened URL by its ID."""
        return await self.repo.get_by_id(url_id)

    async def get_url_by_short_code(self, short_code: str) -> URL | None:
        """Retrieve a shortened URL by its short code."""
        return await self.repo.get_by_short_code(short_code)

    async def get_url_by_original_url(self, original_url: str, owner_id: str | None = None) -> URL | None:
        """Retrieve a shortened URL by its original URL and optional owner ID."""
        return await self.repo.get_by_original_url(original_url, owner_id)

    async def get_all_urls_by_owner(self, owner_id: str) -> list[URL]:
        """Retrieve all shortened URLs for a given owner."""
        return await self.repo.get_all_by_owner(owner_id)


    async def redirect_to_original_url(self, short_code: str) -> str:
        """Redirect to the original URL for a given short code."""
        url = await self.repo.get_by_short_code(short_code)

        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Short URL not found",
            )

        if not url.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This short URL is deactivated",
            )

        if url.expires_at and url.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="This short URL has expired",
            )

        # Increment the click count
        await self.repo.increment_click_count(url.id)

        return url.original_url
























