from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.schemas.token import Token
from app.schemas.officer import Officer, OfficerInDB
from app.models.officer import Officer as OfficerMD

# from app.models.msg import Msg

from app.core import security
from app.core.config import settings


router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user_db = (
        db.query(OfficerMD)
        .filter(OfficerMD.name == form_data.username)
        .one_or_none()
    )
    user = OfficerInDB.model_validate(user_db)
    # print(user)
    if (
        user is None
        or security.verify_password(
            plain_password=form_data.password,
            hashed_password=user.hashed_password,
        )
        is False
    ):
        raise HTTPException(
            status_code=400, detail="Incorrect email or password"
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {
        "access_token": security.create_access_token(
            user.uid, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=Officer)
def test_token(
    current_user: Officer = Depends(get_current_user),
) -> Any:
    """
    Test access token
    """
    return current_user
