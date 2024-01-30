from pydantic import BaseModel, ConfigDict


# Shared properties
class InfractionBase(BaseModel):
    vehicle_id: int | None = None
    timestamp: int | None = None
    coments: str | None = None


# Properties to receive on item creation
class InfractionCreate(InfractionBase):
    vehicle_id: int
    timestamp: int
    coments: str


# Properties to receive on item update
class InfractionUpdate(InfractionBase):
    pass


# Properties shared by models stored in DB
class InfractionInDBBase(InfractionBase):
    model_config = ConfigDict(from_attributes=True)
    uid: int
    vehicle_id: int
    timestamp: int
    coments: str


# Properties to return to client
class Infraction(InfractionInDBBase):
    pass


# Properties properties stored in DB
class InfractionInDB(InfractionInDBBase):
    pass
