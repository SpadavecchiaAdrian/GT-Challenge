from fastapi import (
    APIRouter,
)


from fastapi.responses import HTMLResponse
from fastapi import Request


from app.core.templates import templates


router = APIRouter(
    # tags=["person"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/login", response_class=HTMLResponse)
async def login_interface(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={"name": "adri"}
    )
