from app.services.CRUD_base import CRUDBase
from app.models.person import Person as PersonMD
from app.schemas.person import Person


class PersonService(CRUDBase):
    pass


person_service = PersonService(PersonMD, Person)
