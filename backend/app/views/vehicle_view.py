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
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
    Vehicle,
)
from pydantic import EmailStr
from app.core import deps
from sqlalchemy.orm import Session
from app.services.vehicle_service import vehicle_service
from fastapi.responses import HTMLResponse
from fastapi import Request


from app.core.templates import templates


router = APIRouter(
    # tags=["vehicle"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def vehicle_interface(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="vehicle.html",
        context={"name": "adri"},
    )


@router.get("/get_vehicle_list", response_class=HTMLResponse)
async def get_vehicle_list(
    request: Request,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    vehicles = vehicle_service.get_multi(db=db, skip=skip, limit=limit)

    context = {}
    context["vehicles"] = [vehicle.dict() for vehicle in vehicles]
    return templates.TemplateResponse(
        request=request,
        name="partial/vehicle/vehicle_list.html",
        context=context,
    )


@router.get("/add_vehicle", response_class=HTMLResponse)
async def add_vehicle(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="partial/vehicle/add_vehicle.html",
    )


@router.post("/add_vehicle_submit", response_class=HTMLResponse)
async def add_vehicle_submit(
    request: Request,
    plate: Annotated[str, Form()],
    brand: Annotated[str, Form()],
    color: Annotated[str, Form()],
    owner_id: Annotated[int, Form()],
    db: Session = Depends(deps.get_db),
):
    context = {}

    created_vehicle = vehicle_service.create(
        db=db,
        obj_in=VehicleCreate(
            plate=plate, brand=brand, color=color, owner_id=owner_id
        ),
    )

    context["vehicle"] = created_vehicle.model_dump()

    return templates.TemplateResponse(
        request=request,
        name="partial/vehicle/vehicle_row.html",
        context=context,
    )


@router.get("/iadd_vehicle_cancel", response_class=HTMLResponse)
async def add_vehicle_cancel(request: Request):
    # return HttpResponse()
    return None


@router.get("/edit_vehicle/{vehicle_id}", response_class=HTMLResponse)
async def edit_vehicle(
    request: Request,
    vehicle_id: int,
    db: Session = Depends(deps.get_db),
):
    vehicle = vehicle_service.get(db, vehicle_id)
    context = {}
    context["vehicle"] = vehicle
    context["form"] = vehicle.model_dump()
    return templates.TemplateResponse(
        request=request,
        name="partial/vehicle/edit_vehicle.html",
        context=context,
    )


@router.get("/edit_vehicle_submit/{vehicle_id}", response_class=HTMLResponse)
async def cancel_edit_vehicle_submit(
    request: Request,
    vehicle_id: int,
    db: Session = Depends(deps.get_db),
):
    context = {}
    vehicle = vehicle_service.get(db, vehicle_id)
    context["vehicle"] = vehicle.model_dump()

    return templates.TemplateResponse(
        request=request,
        name="partial/vehicle/vehicle_row.html",
        context=context,
    )


@router.post("/edit_vehicle_submit/{vehicle_id}", response_class=HTMLResponse)
async def edit_vehicle_submit(
    request: Request,
    vehicle_id: int,
    plate: Annotated[str | None, Form()],
    brand: Annotated[str | None, Form()],
    color: Annotated[str | None, Form()],
    owner_id: Annotated[int | None, Form()],
    db: Session = Depends(deps.get_db),
):
    update = VehicleUpdate(
        plate=plate, brand=brand, color=color, owner_id=owner_id
    )
    vehicle = vehicle_service.update(db=db, uid=vehicle_id, obj=update)
    context = {}
    context["vehicle"] = vehicle.model_dump()

    return templates.TemplateResponse(
        request=request,
        name="partial/vehicle/vehicle_row.html",
        context=context,
    )


@router.delete("/delete_vehicle/{vehicle_id}", response_class=HTMLResponse)
async def delete_vehicle(
    request: Request,
    vehicle_id: int,
    db: Session = Depends(deps.get_db),
):
    delete_result = vehicle_service.remove(db=db, uid=vehicle_id)
    if delete_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {vehicle_id} not found",
        )
