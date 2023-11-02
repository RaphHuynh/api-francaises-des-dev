import jwt
import secrets

from app import settings
from app.lib.sql import *

from datetime import datetime, timedelta
from fastapi import APIRouter, Response
from fastapi_sso.sso.github import GithubSSO
from starlette.requests import Request
from starlette.responses import RedirectResponse


router = APIRouter(
    prefix="/github",
    tags=["github"]
)

github_sso = GithubSSO(
    settings.GITHUB["client_id"],
    settings.GITHUB["client_secret"],
    f"{settings.GITHUB['callback_uri']}/github/callback"
)


@router.get("/login")
async def github_login():
    return await github_sso.get_login_redirect()


@router.get("/callback")
async def github_callback(request: Request) -> Response:
    user = await github_sso.verify_and_process(request)
    member = await get_member_by_username(user.display_name)

    member_id = member.id if member else await register_new_member(user.display_name)
    if not member_id:
        return Response(status_code=500)

    access_token = secrets.token_hex(16)
    refresh_token = secrets.token_hex(16)

    session = await get_session(member_id)
    token_data = {"user_id": member_id, "access_token": access_token, "refresh_token": refresh_token}

    if not session:
        await register_token(access_token, refresh_token, member_id)
    elif session.date_created + timedelta(minutes=60) > datetime.now():
        token_data = {"user_id": session.id_member, "access_token": session.access_token, "refresh_token": session.refresh_token}
    else:
        await delete_session(member_id)
        await register_token(access_token, refresh_token, member_id)

    print(token_data)
    response = RedirectResponse(url=f"http://127.0.0.1:5173/profil/{member_id}")
    
    response.set_cookie(
        key="token_user",
        value={"id_member": member_id},
        httponly=False
    )
    response.set_cookie(
        key="access_token",
        value=jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM),
        httponly=True
    )

    return response
