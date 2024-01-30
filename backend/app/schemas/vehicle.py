from pydantic import BaseModel, ConfigDict


# Shared properties
class VehicleBase(BaseModel):
    plate: str | None = None
    brand: str | None = None
    color: str | None = None
    owner_id: int | None = None


# Properties to receive on item creation
class VehicleCreate(VehicleBase):
    plate: str
    brand: str
    color: str
    owner_id: int


# Properties to receive on item update
class VehicleUpdate(VehicleBase):
    pass


# Properties shared by models stored in DB
class VehicleInDBBase(VehicleBase):
    model_config = ConfigDict(from_attributes=True)
    uid: int
    plate: str
    brand: str
    color: str
    owner_id: int


# Properties to return to client
class Vehicle(VehicleInDBBase):
    pass


# Properties properties stored in DB
class VehicleInDB(VehicleInDBBase):
    pass
