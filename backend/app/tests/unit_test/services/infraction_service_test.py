import pytest
from sqlalchemy.orm import Session
from app.models.infraction import Infraction as InfractionMD
from app.schemas.infraction import (
    Infraction,
    InfractionCreate,
    InfractionUpdate,
)
from app.services.infraction_service import infraction_service


@pytest.fixture
def clean_infractions(db: Session):
    yield None
    db.query(InfractionMD).delete()


@pytest.fixture
def one_infraction(db: Session, clean_infractions):
    p1 = InfractionMD(vehicle_id=1, timestamp=1706576502, coments="high speed")
    db.add(p1)
    db.commit()
    db.refresh(p1)
    return Infraction.model_validate(p1)


@pytest.fixture
def some_infractions(db: Session, clean_infractions):
    infractions = [
        InfractionMD(vehicle_id=1, timestamp=1706576502, coments="high speed"),
        InfractionMD(
            vehicle_id=1, timestamp=1706576505, coments="crosses a red light"
        ),
        InfractionMD(
            vehicle_id=2, timestamp=1706576508, coments="badly parked"
        ),
    ]
    db.add_all(infractions)
    db.commit()
    to_return = []
    for infraction in infractions:
        to_return.append(Infraction.model_validate(infraction))
    return to_return


# Test cases


def test_should_create_infraction(db: Session, clean_infractions):
    """when an infraction is save, an id is assigned into the db,
    as result, the infraction representation should be returned as
    part of the response
    """
    input_infraction = InfractionCreate(
        vehicle_id=1, timestamp=1706576505, coments="high speed"
    )
    saved_infraction = infraction_service.create(
        db=db, obj_in=input_infraction
    )
    assert isinstance(saved_infraction, Infraction)
    assert isinstance(saved_infraction.uid, int)
    assert saved_infraction.coments == input_infraction.coments


def test_should_get_infraction(db: Session, one_infraction: Infraction):
    retrieved_infraction = infraction_service.get(
        db=db, uid=one_infraction.uid
    )

    assert isinstance(retrieved_infraction, Infraction)


def test_should_get_none_when_id_not_exist(
    db: Session,
):
    non_existing_id = 99
    retrieved_infraction = infraction_service.get(db=db, uid=non_existing_id)

    assert retrieved_infraction is None


def test_should_list_infractions(
    db: Session, some_infractions: list[Infraction]
):
    infractions = infraction_service.get_multi(db=db)

    assert isinstance(infractions, list)
    assert isinstance(infractions[0], Infraction)
    assert isinstance(infractions[1], Infraction)


def test_should_allow_infraction_partial_update(
    db: Session, one_infraction: Infraction
):
    update_data = InfractionUpdate(coments="change")
    updated_infraction = infraction_service.update(
        db=db, uid=one_infraction.uid, obj=update_data
    )
    assert updated_infraction.coments == update_data.coments


def test_should_return_none_if_partial_update_an_inexistent_infraction(
    db: Session,
):
    update_data = InfractionUpdate(coments="change")
    updated_infraction = infraction_service.update(
        db=db, uid=9, obj=update_data
    )

    assert updated_infraction is None


def test_should_return_true_infraction_remove_with_id_existing(
    db: Session, one_infraction: Infraction
):
    deleted = infraction_service.remove(db=db, uid=one_infraction.uid)

    assert deleted


def test_should_return_false_infraction_remove_with_non_existing_id(
    db: Session,
):
    deleted = infraction_service.remove(db=db, uid=9)

    assert not deleted
