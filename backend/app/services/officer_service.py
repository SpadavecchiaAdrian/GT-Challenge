from sqlalchemy.orm import Session
from app.services.CRUD_base import CRUDBase
from app.models.officer import Officer as OfficerMD
from app.schemas.officer import Officer, OfficerCreate
from app.core.security import get_password_hash


class OfficerService(CRUDBase):
    def create(self, db: Session, *, obj_in: OfficerCreate) -> Officer:
        db_obj = OfficerMD(
            name=obj_in.name,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return Officer.model_validate(db_obj)


officer_service = OfficerService(OfficerMD, Officer)
