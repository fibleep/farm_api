from fastapi.routing import APIRouter

from farm_api.web.api import textgen

api_router = APIRouter()
api_router.include_router(textgen.router)
