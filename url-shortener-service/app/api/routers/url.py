from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_user, get_db, get_redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import User
from app.schemas.url import CreateURLRequest
from app.repositories.url_repository import URLRepository
from app.services.url_service import URLService
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/url", tags=["url"])

from redis.asyncio import Redis

# Create, Update and Delete URL endpoints

@router.post("/create")
async def create_url(
    url_req: CreateURLRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    url_service = URLService(
        repo=URLRepository(db),
        redis=redis,
    )

    return await url_service.create_url(
        create_url_request=url_req,
        user=current_user,
    )

@router.delete("/{url_id}")
async def delete_url(
        url_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    url_service = URLService(
        repo=URLRepository(db),
        redis=None,  # Redis is not needed for deletion
    )

    await url_service.delete_url(
        url_id=url_id,
        user=current_user,
    )

    return {"message": "URL deleted successfully"}

@router.post("/{url_id}/deactivate")
async def deactivate_url(
        url_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    url_service = URLService(
        repo=URLRepository(db),
        redis=None,  # Redis is not needed for deactivation
    )

    await url_service.deactivate_url(
        url_id=url_id,
        user=current_user,
    )

    return {"message": "URL deactivated successfully"}

@router.post("/{url_id}/activate")
async def activate_url(
        url_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    url_service = URLService(
        repo=URLRepository(db),
        redis=None,  # Redis is not needed for activation
    )

    await url_service.activate_url(
        url_id=url_id,
        user=current_user,
    )

    return {"message": "URL activated successfully"}

@router.post("/{url_id}/update_expiration")
async def update_url_expiration(
        url_id: int,
        expires_at: str,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    url_service = URLService(
        repo=URLRepository(db),
        redis=None,  # Redis is not needed for updating expiration
    )

    await url_service.update_url_expiration(
        url_id=url_id,
        expires_at=expires_at,
        user=current_user,
    )

    return {"message": "URL expiration updated successfully"}

# Read URL endpoints

@router.get("/{url_id}")
async def get_url_by_id(
        url_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    url_service = URLService(
        repo=URLRepository(db),
        redis=None,  # Redis is not needed for fetching URL by ID
    )

    return await url_service.get_url_by_id(url_id)

@router.get("/short_code/{short_code}")
async def get_url_by_short_code(
        short_code: str,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    url_service = URLService(
        repo=URLRepository(db),
        redis=None,  # Redis is not needed for fetching URL by short code
    )

    return await url_service.get_url_by_short_code(short_code)

@router.get("/")
async def get_all_urls_by_owner(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    url_service = URLService(
        repo=URLRepository(db),
        redis=None,  # Redis is not needed for fetching all URLs by owner
    )

    return await url_service.get_all_urls_by_owner(
        owner_id=current_user.id,
    )

@router.get("/original_url")
async def get_url_by_original_url(
        original_url: str,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    url_service = URLService(
        repo=URLRepository(db),
        redis=None,  # Redis is not needed for fetching URL by original URL
    )

    return await url_service.get_url_by_original_url(
        original_url=original_url,
        owner_id=current_user.id,
    )

@router.get("/redirect/{short_code}")
async def redirect_to_original_url(
        short_code: str,
        db: AsyncSession = Depends(get_db),
        redis: Redis = Depends(get_redis),
):
    url_service = URLService(
        repo=URLRepository(db),
        redis=redis,
    )

    original_url = await url_service.redirect_to_original_url(short_code)

    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shortened URL not found or has expired",
        )

    return RedirectResponse(url=original_url)

















