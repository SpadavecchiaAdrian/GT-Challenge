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


@router.post(
    "/",
    response_description="Add new officer",
    status_code=status.HTTP_201_CREATED,
)
def create_officer(
    db: Session = Depends(deps.get_db),
    officer: OfficerCreate = Body(...),
    # officer_service: OfficerService = Depends(officer_service),
):
    created_officer = officer_service.create(db=db, obj_in=officer)

    return created_officer


@router.get(
    "/",
    # response_model=list[Officer],
    response_description="List all officers",
)
def list_officers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> list[Officer]:
    return officer_service.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{officer_id}", response_description="Get a single officer")
def show_officer(
    officer_id: int,
    db: Session = Depends(deps.get_db),
) -> Officer:
    officer = officer_service.get(db, officer_id)
    if officer:
        return officer
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Officer {officer_id} not found",
        )


@router.patch("/{officer_id}", response_description="Update a officer")
def update_officer(
    officer_id: int,
    officer: OfficerUpdate = Body(...),
    db: Session = Depends(deps.get_db),
) -> Officer:
    officer_update = officer_service.update(db=db, uid=officer_id, obj=officer)

    if officer_update is not None:
        return officer_update
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Officer {officer_id} not found",
        )


@router.delete("/{officer_id}", response_description="Delete Officer")
def delete_officer(
    officer_id: int,
    db: Session = Depends(deps.get_db),
):
    delete_result = officer_service.remove(db=db, uid=officer_id)

    if delete_result is not None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Officer {officer_id} not found",
        )
