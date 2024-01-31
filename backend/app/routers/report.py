from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    # Path,
    # Request,
)

# from fastapi.responses import Response
from pydantic import EmailStr
from app.schemas.infraction import Infraction
from app.core import deps
from sqlalchemy.orm import Session
from app.services.infraction_service import infraction_service


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/generar_informe/{email}",
    response_description="Get a report of all infractions",
)
def show_vehicle(
    email: EmailStr,
    db: Session = Depends(deps.get_db),
) -> list[Infraction]:
    vehicle = infraction_service.get_all_by_person_email(db, email)
    if vehicle:
        return vehicle
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {email} not found",
        )
