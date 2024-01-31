from app.models.infraction import Infraction as InfractionMD
from app.models.vehicle import Vehicle as VehicleMD
from app.models.person import Person as PersonMD
from app.schemas.infraction import Infraction, InfractionCreate
from app.services.person_service import PersonException

from sqlalchemy.orm import Session


class VehicleException(Exception):
    pass


class InfractionService:
    def create(self, db: Session, obj_in: InfractionCreate) -> Infraction:
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
            raise VehicleException(
                f"Vehicle with plate {obj_in.plate} does not exist"
            )

    def get_all_by_person_email(self, db: Session, email: str):
        person = (
            db.query(PersonMD).filter(PersonMD.email == email).one_or_none()
        )
        if person is None:
            raise PersonException(f"No person with email {email} was found")

        # infractions = (
        #     db.query(InfractionMD)
        #     .join(VehicleMD)
        #     .join(PersonMD)
        #     .filter(PersonMD.email == email)
        #     .all()
        # )
        vehicles = [vehicle.uid for vehicle in person.vehicles]
        print(vehicles)
        infractions = (
            db.query(InfractionMD)
            .join(VehicleMD)
            .filter(VehicleMD.uid.in_(vehicles))
            .all()
        )
        infractions_list = []
        for infaction in infractions:
            infractions_list.append(Infraction.model_validate(infaction))
        return infractions_list


infraction_service = InfractionService()
