from fastapi import FastAPI

from app.routers import persons, vehicles, officers, infractions, login


# Solo para test, crear tablas
from app.db.database import Base, engine
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(login.router, prefix=settings.API_V1_STR, tags=["login"])
app.include_router(
    persons.router, prefix=f"{settings.API_V1_STR}/people", tags=["person"]
)
app.include_router(
    vehicles.router, prefix=f"{settings.API_V1_STR}/vehicle", tags=["vehicle"]
)
app.include_router(
    officers.router,
    prefix=f"{settings.API_V1_STR}/officer",
    tags=["officer"],
)
app.include_router(
    infractions.router,
    tags=["infraction"],
)
