
from typing import Optional
from app.schemas.user_schema import UserAuth
from app.models.user_model import User
from app.core.security import get_password, verify_password
from uuid import UUID

class UserService:
    @staticmethod
    async def create(user: UserAuth):
        user_obj = User(
            username = user.username,
            email = user.email,
            hashed_password = get_password(user.password),
            first_name = user.first_name,
            last_name = user.last_name,
            disabled = False
        )
        await user_obj.save()
        return user_obj

    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await UserService.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password=password, hashed_pass=User.hashed_password):
            return None
        
        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        user = await User.find_one(User.email == email)
        return user
    
    @staticmethod
    async def get_user_by_id(user_id: UUID) -> Optional[User]:
        user = await User.find_one(User.user_id == user_id)
        return user
