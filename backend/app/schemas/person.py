from pydantic import BaseModel, ConfigDict, EmailStr


# Shared properties
class PersonBase(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


# Properties to receive on item creation
class PersonCreate(PersonBase):
    name: str
    email: EmailStr


# Properties to receive on item update
class PersonUpdate(PersonBase):
    pass


# Properties shared by models stored in DB
class PersonInDBBase(PersonBase):
    model_config = ConfigDict(from_attributes=True)
    uid: int
    name: str
    email: EmailStr


# Properties to return to client
class Person(PersonInDBBase):
    pass


# Properties properties stored in DB
class PersonInDB(PersonInDBBase):
    pass
