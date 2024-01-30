from pydantic import BaseModel, ConfigDict


# Shared properties
class OfficerBase(BaseModel):
    name: str | None = None


# Properties to receive on item creation
class OfficerCreate(OfficerBase):
    name: str


# Properties to receive on item update
class OfficerUpdate(OfficerBase):
    pass


# Properties shared by models stored in DB
class OfficerInDBBase(OfficerBase):
    model_config = ConfigDict(from_attributes=True)
    uid: int
    name: str


# Properties to return to client
class Officer(OfficerInDBBase):
    pass


# Properties properties stored in DB
class OfficerInDB(OfficerInDBBase):
    pass
