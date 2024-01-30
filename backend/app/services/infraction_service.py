from app.models.infraction import Infraction as InfractionMD
from app.models.vehicle import Vehicle as VehicleMD
from app.schemas.infraction import Infraction, InfractionCreate


from sqlalchemy.orm import Session


class VehicleNoExist(Exception):
    pass


class InfractionService:
    def create(self, db: Session, *, obj_in: InfractionCreate) -> Infraction:
        vehicle = (
            db.query(VehicleMD)
            .filter(VehicleMD.plate == obj_in.plate)
            .one_or_none()
        )
        if vehicle is not None:
            db_obj = InfractionMD(
                vehicle_id=vehicle.uid,
                timestamp=obj_in.timestamp,
                comments=obj_in.comments,
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return Infraction.model_validate(db_obj)
        else:
            raise VehicleNoExist(
                f"Vehicle with plate {obj_in.plate} does not exist"
            )


infraction_service = InfractionService()
