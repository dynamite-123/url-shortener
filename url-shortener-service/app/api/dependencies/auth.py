from fastapi import Depends, Header, HTTPException, status

from app.schemas.auth import VerifyTokenResponse
from app.services.auth_client import AuthClient
from app.services.dependencies import get_auth_client
from app.core.security import extract_bearer_token


async def get_current_user(
    authorization: str = Header(...),
    auth_client: AuthClient = Depends(get_auth_client),
) -> VerifyTokenResponse:
    token = extract_bearer_token(authorization)

    try:
        user = await auth_client.verify_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return user