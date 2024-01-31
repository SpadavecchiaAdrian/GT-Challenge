from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Form,
    # Path,
    # Request,
)
from typing import Annotated
from app.schemas.person import (
    PersonCreate,
    PersonUpdate,
    Person,
)
from pydantic import EmailStr
from app.core import deps
from sqlalchemy.orm import Session
from app.services.person_service import person_service
from fastapi.responses import HTMLResponse
from fastapi import Request


from app.core.templates import templates


router = APIRouter(
    # tags=["person"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def person_interface(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="person.html",
        context={"name": "adri"},
    )


@router.get("/get_person_list", response_class=HTMLResponse)
async def get_person_list(
    request: Request,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    people = person_service.get_multi(db=db, skip=skip, limit=limit)

    context = {}
    context["people"] = [person.dict() for person in people]
    return templates.TemplateResponse(
        request=request,
        name="partial/person/person_list.html",
        context=context,
    )


@router.get("/add_person", response_class=HTMLResponse)
async def add_person(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="partial/person/add_person.html",
    )


@router.post("/add_person_submit", response_class=HTMLResponse)
async def add_person_submit(
    request: Request,
    name: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    db: Session = Depends(deps.get_db),
):
    context = {}

    created_person = person_service.create(
        db=db, obj_in=PersonCreate(name=name, email=email)
    )

    context["person"] = created_person.model_dump()

    return templates.TemplateResponse(
        request=request,
        name="partial/person/person_row.html",
        context=context,
    )


@router.get("/iadd_person_cancel", response_class=HTMLResponse)
async def add_person_cancel(request: Request):
    # return HttpResponse()
    return None


@router.get("/edit_person/{person_id}", response_class=HTMLResponse)
async def edit_person(
    request: Request,
    person_id: int,
    db: Session = Depends(deps.get_db),
):
    person = person_service.get(db, person_id)
    context = {}
    context["person"] = person
    context["form"] = person.model_dump()
    return templates.TemplateResponse(
        request=request,
        name="partial/person/edit_person.html",
        context=context,
    )


@router.get("/edit_person_submit/{person_id}", response_class=HTMLResponse)
async def cancel_edit_person_submit(
    request: Request,
    person_id: int,
    db: Session = Depends(deps.get_db),
):
    context = {}
    person = person_service.get(db, person_id)
    context["person"] = person.model_dump()

    return templates.TemplateResponse(
        request=request,
        name="partial/person/person_row.html",
        context=context,
    )


@router.post("/edit_person_submit/{person_id}", response_class=HTMLResponse)
async def edit_person_submit(
    request: Request,
    person_id: int,
    name: Annotated[str | None, Form()],
    email: Annotated[EmailStr | None, Form()],
    db: Session = Depends(deps.get_db),
):
    update = PersonUpdate(name=name, email=email)
    person = person_service.update(db=db, uid=person_id, obj=update)
    context = {}
    context["person"] = person.model_dump()

    return templates.TemplateResponse(
        request=request,
        name="partial/person/person_row.html",
        context=context,
    )


@router.delete("/delete_person/{person_id}", response_class=HTMLResponse)
async def delete_person(
    request: Request,
    person_id: int,
    db: Session = Depends(deps.get_db),
):
    delete_result = person_service.remove(db=db, uid=person_id)
    if delete_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person {person_id} not found",
        )
