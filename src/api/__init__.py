from fastapi import APIRouter


from src.api.v1.snippets import snippets_router
from src.api.v1.user import user_router
from src.api.v1.auth import auth_router

api_router = APIRouter()

api_router.include_router(snippets_router)
api_router.include_router(user_router)
api_router.include_router(auth_router)