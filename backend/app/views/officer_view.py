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
from app.schemas.officer import (
    OfficerCreate,
    OfficerUpdate,
    Officer,
)
from app.core import deps
from sqlalchemy.orm import Session
from app.services.officer_service import officer_service
from fastapi.responses import HTMLResponse
from fastapi import Request


from app.core.templates import templates


router = APIRouter(
    # tags=["officer"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def officer_interface(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="officer.html",
        context={"name": "adri"},
    )


@router.get("/get_officer_list", response_class=HTMLResponse)
async def get_officer_list(
    request: Request,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    officers = officer_service.get_multi(db=db, skip=skip, limit=limit)

    context = {}
    context["officers"] = [officer.dict() for officer in officers]
    return templates.TemplateResponse(
        request=request,
        name="partial/officer/officer_list.html",
        context=context,
    )


@router.get("/add_officer", response_class=HTMLResponse)
async def add_officer(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="partial/officer/add_officer.html",
    )


@router.post("/add_officer_submit", response_class=HTMLResponse)
async def add_officer_submit(
    request: Request,
    name: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(deps.get_db),
):
    context = {}

    created_officer = officer_service.create(
        db=db,
        obj_in=OfficerCreate(name=name, password=password),
    )

    context["officer"] = created_officer.model_dump()

    return templates.TemplateResponse(
        request=request,
        name="partial/officer/officer_row.html",
        context=context,
    )


@router.get("/iadd_officer_cancel", response_class=HTMLResponse)
async def add_officer_cancel(request: Request):
    # return HttpResponse()
    return None


@router.get("/edit_officer/{officer_id}", response_class=HTMLResponse)
async def edit_officer(
    request: Request,
    officer_id: int,
    db: Session = Depends(deps.get_db),
):
    officer = officer_service.get(db, officer_id)
    context = {}
    context["officer"] = officer
    context["form"] = officer.model_dump()
    return templates.TemplateResponse(
        request=request,
        name="partial/officer/edit_officer.html",
        context=context,
    )


@router.get("/edit_officer_submit/{officer_id}", response_class=HTMLResponse)
async def cancel_edit_officer_submit(
    request: Request,
    officer_id: int,
    db: Session = Depends(deps.get_db),
):
    context = {}
    officer = officer_service.get(db, officer_id)
    context["officer"] = officer.model_dump()

    return templates.TemplateResponse(
        request=request,
        name="partial/officer/officer_row.html",
        context=context,
    )


@router.post("/edit_officer_submit/{officer_id}", response_class=HTMLResponse)
async def edit_officer_submit(
    request: Request,
    officer_id: int,
    name: Annotated[str | None, Form()],
    db: Session = Depends(deps.get_db),
):
    update = OfficerUpdate(name=name)
    officer = officer_service.update(db=db, uid=officer_id, obj=update)
    context = {}
    context["officer"] = officer.model_dump()

    return templates.TemplateResponse(
        request=request,
        name="partial/officer/officer_row.html",
        context=context,
    )


@router.delete("/delete_officer/{officer_id}", response_class=HTMLResponse)
async def delete_officer(
    request: Request,
    officer_id: int,
    db: Session = Depends(deps.get_db),
):
    delete_result = officer_service.remove(db=db, uid=officer_id)
    if delete_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Officer {officer_id} not found",
        )
