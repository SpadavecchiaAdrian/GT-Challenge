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

from app.schemas.vehicle import Vehicle, VehicleCreate, VehicleUpdate

from app.core import deps
from sqlalchemy.orm import Session
from app.services.vehicle_service import vehicle_service


router = APIRouter(
    responses={404: {"description": "Not found"}},
)
