from app.lib.sql import *

from typing import List
from fastapi import APIRouter


router = APIRouter(
    prefix="/network",
    tags=["network"]
)


@router.get("/", response_model=List[Network])
async def api_get_network():
    return await get_network()
