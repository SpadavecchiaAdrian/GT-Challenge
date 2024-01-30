from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Body,
    # Path,
    # Request,
)

from app.schemas.infraction import (
    InfractionCreate,
)

from app.core import deps
from sqlalchemy.orm import Session
from app.services.infraction_service import infraction_service, VehicleNoExist

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_description="Add new infraction",
    status_code=status.HTTP_201_CREATED,
)
def create_infraction(
    db: Session = Depends(deps.get_db),
    infraction: InfractionCreate = Body(...),
    # infraction_service: InfractionService = Depends(infraction_service),
):
    try:
        created_infraction = infraction_service.create(
            db=db, obj_in=infraction
        )
    except VehicleNoExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return created_infraction
