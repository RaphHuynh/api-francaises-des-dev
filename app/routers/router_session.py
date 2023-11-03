from typing import Optional, Union, Annotated
import jwt
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.lib.sql import verif_session
from app.models.session import SessionCookie
from app.settings import SECRET_KEY, ALGORITHM
import logging

router = APIRouter(
    prefix="/session",
    tags=["session"]
)

logger = logging.getLogger(__name__)

def get_access_token_from_cookie(request: Request) -> str:
    """Extract the access token from the request cookies."""
    access_token = request.cookies.get('access_token')
    if not access_token:
        raise HTTPException(status_code=401, detail="Authentication token is missing.")
    return access_token

@router.get("/")
async def api_is_connected(access_token: str = Depends(get_access_token_from_cookie)):
    """Check if the user is authenticated based on the access token."""
    try:
        cookie_session_decode = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
        logger.info(f"Decoded session: {cookie_session_decode}")
        if await verif_session(cookie_session_decode):
            return {"status": 200}
        else:
            return {"status": 401}
    except jwt.ExpiredSignatureError:
        return {"status": 401, "detail": "Token has expired"}
    except jwt.JWTError:
        return {"status": 400, "detail": "Invalid token"}
    except Exception as e:
        logger.error(f"Error while verifying session: {e}")
        return {"status": 500, "detail": "Internal Server Error"}

@router.delete("/logout")
async def api_logout(request: Request):
    """Logout the user by deleting the session cookies."""
    response = JSONResponse({"status": 200, "detail": "Successfully logged out"})
    response.delete_cookie(key="access_token")
    return response
