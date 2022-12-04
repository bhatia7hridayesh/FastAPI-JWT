from fastapi import APIRouter
from app.api.api_v1.handlers.user import user_router
from app.api.authentication.jwt import auth_router
router = APIRouter()

router.include_router(user_router, prefix='/users', tags=['users'])
router.include_router(auth_router, prefix='/authentication', tags=['authentication'])
