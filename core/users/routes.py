from fastapi import APIRouter, Path, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from users.schemas import *
from users.models import UserModel
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
import secrets

router = APIRouter(tags=["users"], prefix="/users")



@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = (
        db.query(UserModel)
        .filter_by(username=request.username.lower())
        .first()
    )
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user aor password",
        )
    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user aor password",
        )

    # Token Based Authentication
    # token_obj = TokenModel(user_id = user_obj.id,token=generate_token())
    # db.add(token_obj)
    # db.commit()
    # db.refresh(token_obj)
    return JSONResponse(
        content={
            "detail": "logged in successfully",
        #    "access_token": access_token,
        #    "refresh_token": refresh_token,
        }
    )


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
