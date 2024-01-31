from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException

from fastapi.responses import HTMLResponse
from fastapi import Request

from sqlalchemy.orm import Session

from app.core.templates import templates
from app.core import deps
from app.core import security
from app.core.config import settings
from datetime import timedelta

from app.models.officer import Officer as OfficerMD
from app.schemas.officer import OfficerInDB

router = APIRouter(
    # tags=["person"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/login", response_class=HTMLResponse)
async def login_interface(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"name": "adri"}
    )


@router.post("/generate_token", response_class=HTMLResponse)
async def get_token(
    request: Request,
    name: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(deps.get_db),
):
    user_db = db.query(OfficerMD).filter(OfficerMD.name == name).one_or_none()
    user = OfficerInDB.model_validate(user_db)
    # print(user)
    if (
        user is None
        or security.verify_password(
            plain_password=password,
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
    refresh_token = security.create_access_token(
        user.uid, expires_delta=access_token_expires
    )

    return f"Bearer Token: {refresh_token}"
