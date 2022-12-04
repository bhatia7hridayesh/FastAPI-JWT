from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException, status
from typing import Any
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import ValidationError
from app.api.deps.user_deps import get_current_user
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.models.user_model import User
from app.schemas.auth_schema import TokenPayload, TokenSchema
from app.services.user_service import UserService
from app.schemas.user_schema import UserResponse

auth_router = APIRouter()

@auth_router.post('/login', summary="Create token for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any :
    user = await UserService.authenticate(email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Incorrect Email or Password"
        )

    #create token

    return (
        {
            "access_token": create_access_token(user.user_id),
            #"token_type": "bearer"
            "refresh_token": create_refresh_token(user.user_id)
        }
    )

@auth_router.post("/refresh", summary="Refresh Token", response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=settings.ALGORITHM)
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
    return  {
            "access_token": create_access_token(user.user_id),
            #"token_type": "bearer"
            "refresh_token": create_refresh_token(user.user_id)
        }

@auth_router.post('/test', summary="Test if the user token is valid", response_model = UserResponse)
async def test(user: User = Depends(get_current_user)):
    return user