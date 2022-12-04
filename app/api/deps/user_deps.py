from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from app.core.config import settings
from app.models.user_model import User
from jose import jwt
from datetime import datetime
from app.schemas.auth_schema import TokenPayload
from app.services.user_service import UserService

oauth2_scheme  = OAuth2PasswordBearer(
    tokenUrl = f"{settings.API_V1_STRING}/authentication/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl=f"/api/v1/authentication/login") )):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.ALGORITHM)
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "Token expired",
                headers= {"WW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail= "Could Not Validate Credentials",
                headers= {"WW-Authenticate": "Bearer"},
            )
    user = await UserService.get_user_by_id(token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could Not Find User"
        )
    return user