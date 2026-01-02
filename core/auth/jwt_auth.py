from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from users.models import UserModel, TokenModel
from core.database import get_db
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import DecodeError , InvalidSignatureError 
from datetime import datetime , timedelta , timezone
from core.config import settings
security = HTTPBearer(scheme_name="Token")





def generate_access_token(user_id: int, expires_in: int = 60 * 5) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "type": "access",
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


def generate_refresh_token(user_id: int, expires_in: int = 3600 * 24) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "type": "refresh",
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")

def decode_refresh_token(token):
    try:
        decoded = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms="HS256"
        )
        user_id = decoded.get("user_id", None)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed, user_id not in the payload",
            )

        if decoded.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed, token type not valid",
            )
        if datetime.now() > datetime.fromtimestamp(decoded.get("exp")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed, token expired",
            )

        return user_id

    except InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed, invalid signature",
        )
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed, decode failed",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed, {e}",
        )