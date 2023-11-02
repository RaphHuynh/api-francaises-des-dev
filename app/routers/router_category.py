from app.models import *
from app.lib.sql import *

from typing import List
from fastapi import APIRouter
from starlette.responses import Response


router = APIRouter(
    prefix="/category",
    tags=["category"]
)


@router.get("/", response_model=List[Category])
async def api_get_categories():
    return await get_categories()


@router.post("/")
async def api_post_category(category: CategoryOut):
    return Response(status_code = await post_category(category))
