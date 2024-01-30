from pydantic import BaseModel, ConfigDict


# Shared properties
class InfractionBase(BaseModel):
    timestamp: int | None = None
    comments: str | None = None


# Properties to receive on item creation
class InfractionCreate(InfractionBase):
    plate: str
    timestamp: int
    comments: str


# Properties to receive on item update
class InfractionUpdate(InfractionBase):
    plate: str


# Properties shared by models stored in DB
class InfractionInDBBase(InfractionBase):
    model_config = ConfigDict(from_attributes=True)
    uid: int
    vehicle_id: int
    timestamp: int
    comments: str


# Properties to return to client
class Infraction(InfractionInDBBase):
    pass


# Properties properties stored in DB
class InfractionInDB(InfractionInDBBase):
    pass
