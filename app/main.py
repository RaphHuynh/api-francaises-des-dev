from typing import List

from starlette.middleware.cors import CORSMiddleware

from app.lib.sql import *

from fastapi import FastAPI, Response, UploadFile
from app.models import MemberIn, MemberOut, Category, CategoryOut, MemberWithCategory, MemberHasCategoryIn, \
    GetMemberHasNetwork, MemberById, Network, MemberHasNetwork, MemberHasCategory, MemberHasNetworkIn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/members", response_model=List[MemberWithCategory])
async def api_get_members():
    return await get_members()


@app.get("/members/{id:int}", response_model=MemberIn)
async def api_get_member_by_id(id: int):
    member = await get_member_by_id(id)
    if member is None:
        return Response(status_code=404)
    return member


@app.post("/members", response_model=MemberOut)
def api_post_member(member: MemberIn):
    result = post_member(member)
    if result is not None:
        return Response(status_code=400)
    return Response(status_code=200)


@app.patch("/members")
def api_patch_member_update(member: MemberOut):
    result = patch_member_update(member)
    if result is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@app.get("/categories", response_model=List[Category])
async def api_get_categories():
    return await get_categories()


@app.post("/categories")
def api_post_category(category: CategoryOut):
    result = post_category(category)
    if result is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@app.get("/members/category={name:str}")
async def api_get_members_category(name: str):
    member = await get_members_category(name)
    if member is None:
        return Response(status_code=404)
    return member


@app.post("/members/category")
def api_post_add_category_on_member(member: MemberHasCategoryIn):
    category = post_add_category_on_member(member)
    if category is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@app.get("/network", response_model=List[Network])
async def api_get_network():
    return await get_network()


@app.get("/members/network", response_model=List[GetMemberHasNetwork])
async def api_get_network_of_member(id_member: int):
    return await get_network_of_member_by_id(id_member)


@app.get("/members/list_category", response_model=List[CategoryOut])
async def api_get_category_of_member_by_id(member: MemberById):
    return await get_category_of_member_by_id(member)


@app.post("/members/network")
def api_post_network_on_member(member: MemberHasNetwork):
    network = post_network_on_member(member)
    if network is not None:
        return Response(status_code=400)
    return Response(status_code=201)


@app.delete("/members/category")
def api_delete_category_delete_by_member(member: MemberHasCategory):
    verif = delete_category_delete_by_member(member)
    if verif is not None:
        return Response(status_code=400)
    return Response(status_code=200)


@app.delete("/members/network")
def api_delete_network_delete_by_member(member: MemberHasNetworkIn):
    verif = delete_network_delete_by_member(member)
    if verif is not None:
        return Response(status_code=400)
    return Response(status_code=200)


@app.post("/members/image_portfolio")
def api_add_image_portfolio(file: UploadFile, id_member: int):
    if file.size > 200*10000:
        return Response(status_code=413)
    if file.content_type not in ['image/jpeg', 'image/png']:
        return Response(status_code=415)
    verif = add_image_portfolio(file, id_member)
    if verif is not None:
        return Response(status_code=500)
    return Response(status_code=200)


@app.get("/members/image_portfolio_by_id")
async def api_get_image_portfolio_by_id_member(id_member: int):
    return Response(content=await get_image_by_id_member(id_member), media_type="image/jpg")
