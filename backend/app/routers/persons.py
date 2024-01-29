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
from app.schemas.person import (
    PersonCreate,
    PersonUpdate,
    Person,
)

from app.core import deps
from sqlalchemy.orm import Session
from app.services.person_service import person_service


router = APIRouter(
    # tags=["person"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_description="Add new person",
    status_code=status.HTTP_201_CREATED,
)
def create_person(
    db: Session = Depends(deps.get_db),
    person: PersonCreate = Body(...),
    # person_service: PersonService = Depends(person_service),
):
    created_person = person_service.create(db=db, obj_in=person)

    return created_person


@router.get(
    "/",
    # response_model=list[Person],
    response_description="List all persons",
)
def list_persons(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> list[Person]:
    return person_service.get_multi(db=db, skip=skip, limit=limit)


@router.get("/{person_id}", response_description="Get a single person")
def show_person(
    person_id: int,
    db: Session = Depends(deps.get_db),
) -> Person:
    person = person_service.get(db, person_id)
    if person:
        return person
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person {person_id} not found",
        )


@router.patch("/{person_id}", response_description="Update a person")
def update_person(
    person_id: int,
    person: PersonUpdate = Body(...),
    db: Session = Depends(deps.get_db),
) -> Person:
    person_update = person_service.update(db=db, uid=person_id, obj=person)

    if person_update is not None:
        return person_update
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person {person_id} not found",
        )


@router.delete("/{person_id}", response_description="Delete Person")
def delete_person(
    person_id: int,
    db: Session = Depends(deps.get_db),
):
    delete_result = person_service.remove(db=db, uid=person_id)

    if delete_result is True:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person {person_id} not found",
        )
