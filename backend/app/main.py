from fastapi import FastAPI

from app.routers import persons, vehicles, officers  # , infractions


# Solo para test, crear tablas
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

prefix: str = "/api/v1"

app.include_router(persons.router, prefix=f"{prefix}/people", tags=["person"])
# app.include_router(
#     vehicles.router, prefix=f"{prefix}/vehicle", tags=["vehicle"]
# )
# app.include_router(
#     officers.router,
#     prefix=f"{prefix}/officer",
#     tags=["officer"],
# )
# app.include_router(
#     infractions.router,
#     prefix=f"{prefix}/infraction",
#     tags=["infraction"],
# )
