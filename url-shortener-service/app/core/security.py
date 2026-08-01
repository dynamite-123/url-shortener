from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app.services.auth_client import get_auth_client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_client = Depends(get_auth_client),
):
    user = await auth_client.verify_token(token)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
        )

    return user