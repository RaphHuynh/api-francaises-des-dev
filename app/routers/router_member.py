from app.models import *
from app.lib.sql import *
from app.lib.function import isInvalidImage

from typing import List
from fastapi import APIRouter
from starlette.responses import Response


router = APIRouter(
    prefix="/member",
    tags=["member"]
)


@router.get("/", response_model=List[MemberWithCategory])
async def api_get_members():
    return await get_members()


@router.get("/{id:int}", response_model=MemberIn)
async def api_get_member_by_id(id: int):
    return await get_member_by_id(id) or Response(status_code=404)


@router.patch("/")
async def api_patch_member_update(member: MemberOut):
    return Response(status_code = await patch_member_update(member))


@router.patch("/image_portfolio")
async def api_add_image_portfolio(file: UploadFile, id_member: int):
    if file.size > 200 * 10000:
        return Response(status_code=413)
    
    if file.content_type not in ('image/jpeg', 'image/png') or isInvalidImage(file):
        return Response(status_code=415)
    
    return Response(status_code = await add_image_portfolio(file, id_member))


@router.get("/image_portfolio_by_id")
async def api_get_image_portfolio_by_id_member(id_member: int):
    return Response(content=await get_image_by_id_member(id_member), media_type="image/jpg")


@router.post("/category")
async def api_post_add_category_on_member(member: MemberHasCategory):
    return Response(status_code = await post_add_category_on_member(member))


@router.get("/list_category/{id:int}", response_model=List[CategoryOut])
async def api_get_category_of_member_by_id(id: int):
    return await get_category_of_member_by_id(id)


@router.get("/category/{id:int}", response_model=List[MemberHasCategoryOut])
async def api_get_member_has_category_by_id_member(id: int):
    return await get_member_has_category_by_id_member(id)


@router.delete("/category")
async def api_delete_category_delete_by_member(member: MemberHasCategory):
    return Response(status_code = await delete_category_delete_by_member(member))


@router.get("/category={name:str}")
async def api_get_members_category(name: str):
    return await get_members_category(name) or Response(status_code=404)


@router.get("/network/{id:int}", response_model=List[GetMemberHasNetwork])
async def api_get_network_of_member(id: int):
    return await get_network_of_member_by_id(id)


@router.post("/network")
async def api_post_network_on_member(member: MemberHasNetwork):
    return Response(status_code = await post_network_on_member(member))


@router.delete("/network")
async def api_delete_network_delete_by_member(member: MemberHasNetworkIn):
    return Response(status_code = await delete_network_delete_by_member(member))

