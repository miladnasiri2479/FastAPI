from fastapi import APIRouter, Path, Depends, HTTPException, Query, status , Response , Cookie
from fastapi.responses import JSONResponse
from users.schemas import *
from users.models import UserModel, TokenModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
import secrets
from auth.coockie_jwt import get_authenticated_users
from auth.jwt_auth import (
    generate_access_token,
    generate_refresh_token,
    decode_refresh_token,
)

router = APIRouter(tags=["users"], prefix="/users")


def generate_token(length=32):
    """Generate a secure random token as a string."""
    return secrets.token_hex(length)


@router.post("/login")
async def user_login(
    request: UserLoginSchema,
    response: Response,
    db: Session = Depends(get_db),
):
    user_obj = (
        db.query(UserModel)
        .filter_by(username=request.username.lower())
        .first()
    )

    if not user_obj or not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)

    # Access Token Cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 5,
    )

    # Refresh Token Cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24,
    )

    return {"detail": "logged in successfully"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"detail": "logged out successfully"}



@router.post("/register")
async def user_register(
    request: UserRegisterSchema, db: Session = Depends(get_db)
):
    if (
        db.query(UserModel)
        .filter_by(username=request.username.lower())
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username already exists",
        )
    user_obj = UserModel(username=request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED,content={"detail": "user registered successfully"})


@router.post("/refresh-token")
async def refresh_token(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    user_id = decode_refresh_token(refresh_token)
    new_access_token = generate_access_token(user_id)

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 5,
    )

    return {"detail": "access token refreshed"}