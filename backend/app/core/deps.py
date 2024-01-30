from app.db.database import SessionLocal
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from fastapi import HTTPException, Depends, status
from app.models.officer import Officer as OfficerMD
from app.schemas.officer import Officer

from app.core.config import settings

from app.core import security
from pydantic import ValidationError


def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> Officer:
    try:
        token_data = security.decode_access_token(token)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = (
        db.query(OfficerMD)
        .filter(OfficerMD.uid == token_data.sub)
        .one_or_none()
    )
    if not user:
        raise HTTPException(status_code=404, detail="Officer not found")
    return Officer.model_validate(user)
