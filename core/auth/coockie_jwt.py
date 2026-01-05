from fastapi import Depends, HTTPException, status , Cookie
from sqlalchemy.orm import Session
from core.config import settings
from core.database import get_db
from users.models import UserModel
import jwt




def get_authenticated_users(
    access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        decoded = jwt.decode(
            access_token,
            settings.JWT_SECRET_KEY,
            algorithms="HS256",
        )

        if decoded.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = decoded.get("user_id")
        user = db.query(UserModel).filter_by(id=user_id).one()
        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Access token expired",
        )
