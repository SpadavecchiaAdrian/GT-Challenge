from app.services.CRUD_base import CRUDBase
from app.models.officer import Officer as OfficerMD
from app.schemas.officer import Officer


class OfficerService(CRUDBase):
    pass


officer_service = OfficerService(OfficerMD, Officer)
