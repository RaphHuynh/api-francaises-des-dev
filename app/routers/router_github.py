import secrets
from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Response, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.lib.sql import get_member_by_username, register_new_member, get_session, delete_session, register_token
from app.settings import GITHUB, SECRET_KEY, ALGORITHM
from fastapi_sso.sso.github import GithubSSO

router = APIRouter(
    prefix="/github",
    tags=["github"]
)

github_sso = GithubSSO(GITHUB["client_id"], GITHUB["client_secret"], f"{GITHUB['callback_uri']}/github/callback")

@router.get("/login")
async def github_login() -> RedirectResponse:
    """
    Generate GitHub login URL and redirect the user to it.
    """
    return await github_sso.get_login_redirect()

@router.get("/callback")
async def github_callback(request: Request) -> Response:
    """
    Process the callback response from GitHub.
    Authenticate the user and generate the necessary tokens.
    """
    try:
        user = await github_sso.verify_and_process(request)
        member = await get_member_by_username(user.display_name)
        
        if member is None:
            member_id = await register_new_member(user.display_name)
        else:
            member_id = member.id

        access_token = secrets.token_hex(16)
        refresh_token = secrets.token_hex(16)
        session = await get_session(member_id)
        token_data = {"user_id": member_id, "access_token": access_token, "refresh_token": refresh_token}

        if session:
            session_expiry_time = session.date_created + timedelta(minutes=60)
            if session_expiry_time > datetime.now():
                token_data = {
                    "user_id": session.id_member,
                    "access_token": session.access_token,
                    "refresh_token": session.refresh_token
                }
            else:
                await delete_session(member_id)
                await register_token(access_token, refresh_token, member_id)
        else:
            await register_token(access_token, refresh_token, member_id)

        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        token_bis = {"id_member": member_id}

        # Redirect to user profile page
        url_response = f"http://127.0.0.1:5173/profil/{member_id}"
        response = RedirectResponse(url=url_response)

        # Set cookies for tokens
        response.set_cookie(key="access_token", value=token, httponly=True)
        response.set_cookie(key="token_user", value=token_bis, httponly=False)
        return response

    except Exception as e:
        # A more specific exception handling can be added based on different scenarios.
        raise HTTPException(status_code=400, detail=str(e))
