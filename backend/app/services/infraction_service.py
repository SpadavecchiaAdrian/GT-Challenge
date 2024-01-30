from app.services.CRUD_base import CRUDBase
from app.models.infraction import Infraction as InfractionMD
from app.schemas.infraction import Infraction


class InfractionService(CRUDBase):
    pass


infraction_service = InfractionService(InfractionMD, Infraction)
