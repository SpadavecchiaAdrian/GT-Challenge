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

from app.schemas.officer import Officer, OfficerCreate, OfficerUpdate

from app.core import deps
from sqlalchemy.orm import Session
from app.services.officer_service import officer_service

router = APIRouter(
    responses={404: {"description": "Not found"}},
)
