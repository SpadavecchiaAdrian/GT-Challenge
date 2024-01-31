import pytest
from sqlalchemy.orm import Session
from app.models.infraction import Infraction as InfractionMD
from app.models.vehicle import Vehicle as VehicleMD
from app.models.person import Person as PersonMD
from app.schemas.infraction import (
    Infraction,
    InfractionCreate,
)
from app.services.infraction_service import infraction_service


@pytest.fixture
def people_vehicle_infractions(
    db: Session, clean_infractions, clean_vehicles, clean_people
):
    # create a person
    p1 = PersonMD(name="test", email="test@some.com")
    db.add(p1)
    db.commit()
    # create two vehicles
    v1 = VehicleMD(plate="abc123", brand="one", color="blue", owner_id=1)
    v2 = VehicleMD(plate="def456", brand="two", color="green", owner_id=1)
    db.add(v1)
    db.add(v2)
    db.commit()
    db.refresh(v1)
    db.refresh(v2)
    # create many infractions
    i1 = InfractionMD(
        vehicle_id=v1.uid,
        timestamp=1,
        comments="first",
    )
    i2 = InfractionMD(
        vehicle_id=v1.uid,
        timestamp=2,
        comments="second",
    )
    i3 = InfractionMD(
        vehicle_id=v1.uid,
        timestamp=3,
        comments="third",
    )
    i4 = InfractionMD(
        vehicle_id=v2.uid,
        timestamp=4,
        comments="first",
    )

    db.add(i1)
    db.add(i2)
    db.add(i3)
    db.add(i4)
    db.commit()

    return p1.email


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
        infraction_service.create(db=db, obj_in=input_infraction)


def test_should_get_all_infractions_by_person_email(
    db: Session, people_vehicle_infractions
):
    infractions = infraction_service.get_all_by_person_email(
        db=db, email=people_vehicle_infractions
    )

    assert isinstance(infractions, list)
    assert isinstance(infractions[0], Infraction)
    assert isinstance(infractions[1], Infraction)


def test_should_rise_exeption_if_email_doesnt_exist(
    db: Session, people_vehicle_infractions
):
    with pytest.raises(Exception):
        infraction_service.get_all_by_person_email(db=db, email="")
