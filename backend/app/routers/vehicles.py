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


@router.post(
    "/",
    response_description="Add new vehicle",
    status_code=status.HTTP_201_CREATED,
)
def create_vehicle(
    db: Session = Depends(deps.get_db),
    vehicle: VehicleCreate = Body(...),
    # vehicle_service: VehicleService = Depends(vehicle_service),
):
    created_vehicle = vehicle_service.create(db=db, obj_in=vehicle)

    return created_vehicle


@router.get(
    "/",
    # response_model=list[Vehicle],
    response_description="List all vehicles",
)
def list_vehicles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> list[Vehicle]:
    return vehicle_service.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{vehicle_id}", response_description="Get a single vehicle")
def show_vehicle(
    vehicle_id: int,
    db: Session = Depends(deps.get_db),
) -> Vehicle:
    vehicle = vehicle_service.get(db, vehicle_id)
    if vehicle:
        return vehicle
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {vehicle_id} not found",
        )


@router.patch("/{vehicle_id}", response_description="Update a vehicle")
def update_vehicle(
    vehicle_id: int,
    vehicle: VehicleUpdate = Body(...),
    db: Session = Depends(deps.get_db),
) -> Vehicle:
    vehicle_update = vehicle_service.update(db=db, uid=vehicle_id, obj=vehicle)

    if vehicle_update is not None:
        return vehicle_update
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {vehicle_id} not found",
        )


@router.delete("/{vehicle_id}", response_description="Delete Vehicle")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(deps.get_db),
):
    delete_result = vehicle_service.remove(db=db, uid=vehicle_id)

    if delete_result is not None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {vehicle_id} not found",
        )
