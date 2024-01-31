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


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"name": "adri"}
    )
