from __future__ import annotations

from typing import Optional, Union, Annotated

import jwt
from fastapi import APIRouter, Cookie, Header, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from app.lib.sql import verif_session
from app.models.session import SessionCookie
from app.settings import SECRET_KEY, ALGORITHM

router = APIRouter(
    prefix="/session",
    tags=["session"]
)

@router.get("/")
async def api_is_connected(request: Request) -> dict:
    """
    Verifies if a session is connected based on the 'access_token' cookie.

    Args:
        request: The incoming request object.

    Returns:
        dict: A dictionary containing a status code.
    """
    access_token = request.cookies.get('access_token')

    # Check if access_token exists
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found")

    try:
        cookie_session_decode = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
        print(cookie_session_decode)

        if await verif_session(cookie_session_decode):
            return {"status": 200}
        else:
            return {"status": 401}

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="An error occurred while verifying the session")
