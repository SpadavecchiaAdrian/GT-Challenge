import pytest
from sqlalchemy.orm import Session
from app.models.infraction import Infraction as InfractionMD
from app.models.vehicle import Vehicle as VehicleMD
from app.schemas.infraction import (
    Infraction,
    InfractionCreate,
)
from app.services.infraction_service import infraction_service


@pytest.fixture
def clean_infractions(db: Session):
    yield None
    db.query(InfractionMD).delete()
    db.query(VehicleMD).delete()


# Test cases


def test_should_create_infraction(db: Session, clean_infractions):
    """when an infraction is save, an id is assigned into the db,
    as result, the infraction representation should be returned as
    part of the response
    """
    p1 = VehicleMD(plate="abc123", brand="one", color="blue", owner_id=1)
    db.add(p1)
    db.commit()
    input_infraction = InfractionCreate(
        plate="abc123", timestamp=1706576505, comments="high speed"
    )
    saved_infraction = infraction_service.create(
        db=db, obj_in=input_infraction
    )
    assert isinstance(saved_infraction, Infraction)
    assert isinstance(saved_infraction.uid, int)
    assert saved_infraction.comments == input_infraction.comments


def test_should_rise_exeption_if_plate_doesnt_exist(
    db: Session, clean_infractions
):
    input_infraction = InfractionCreate(
        plate="abc123", timestamp=1706576505, comments="high speed"
    )
    with pytest.raises(Exception):
        saved_infraction = infraction_service.create(
            db=db, obj_in=input_infraction
        )
