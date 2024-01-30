from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Body,
    # Path,
    # Request,
)
from fastapi.responses import Response

from app.schemas.infraction import (
    Infraction,
    InfractionCreate,
    InfractionUpdate,
)

from app.core import deps
from sqlalchemy.orm import Session
from app.services.infraction_service import infraction_service

router = APIRouter(
    responses={404: {"description": "Not found"}},
)
