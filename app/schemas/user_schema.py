from typing import Optional
from pydantic import BaseModel, Field
from pydantic import EmailStr
from uuid import UUID


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="user email")
    username: str = Field(..., min_length=1, max_length=50, description="username")
    password: str = Field(..., min_length=5, max_length=24, description="password")
    first_name: str = Field(..., description="First Name")
    last_name: str = Field(..., description="Last Name")

class UserResponse(BaseModel):
    user_id: UUID
    username: str 
    email: EmailStr
    first_name: str
    last_name: str
    disabled: bool 



