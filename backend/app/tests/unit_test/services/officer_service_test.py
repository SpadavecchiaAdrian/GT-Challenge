import pytest
from sqlalchemy.orm import Session
from app.models.officer import Officer as OfficerMD
from app.schemas.officer import (
    Officer,
    OfficerCreate,
    OfficerUpdate,
)
from app.services.officer_service import officer_service


@pytest.fixture
def clean_officers(db: Session):
    yield None
    db.query(OfficerMD).delete()


@pytest.fixture
def one_officer(db: Session, clean_officers):
    p1 = OfficerMD(name="test")
    db.add(p1)
    db.commit()
    db.refresh(p1)
    return Officer.model_validate(p1)


@pytest.fixture
def some_officers(db: Session, clean_officers):
    officers = [
        OfficerMD(name="test1"),
        OfficerMD(name="test2"),
        OfficerMD(name="test3"),
    ]
    db.add_all(officers)
    db.commit()
    to_return = []
    for officer in officers:
        to_return.append(Officer.model_validate(officer))
    return to_return


# Test cases


def test_should_create_officer(db: Session, clean_officers):
    """when an officer is save, an id is assigned into the db,
    as result, the officer representation should be returned as
    part of the response
    """
    input_officer = OfficerCreate(name="test")
    saved_officer = officer_service.create(db=db, obj_in=input_officer)
    assert isinstance(saved_officer, Officer)
    assert isinstance(saved_officer.uid, int)
    assert saved_officer.name == input_officer.name


def test_should_get_officer(db: Session, one_officer: Officer):
    retrieved_officer = officer_service.get(db=db, uid=one_officer.uid)

    assert isinstance(retrieved_officer, Officer)


def test_should_get_none_when_id_not_exist(
    db: Session,
):
    non_existing_id = 99
    retrieved_officer = officer_service.get(db=db, uid=non_existing_id)

    assert retrieved_officer is None


def test_should_list_officers(db: Session, some_officers: list[Officer]):
    officers = officer_service.get_multi(db=db)

    assert isinstance(officers, list)
    assert isinstance(officers[0], Officer)
    assert isinstance(officers[1], Officer)


def test_should_allow_officer_partial_update(
    db: Session, one_officer: Officer
):
    update_data = OfficerUpdate(name="change")
    updated_officer = officer_service.update(
        db=db, uid=one_officer.uid, obj=update_data
    )
    assert updated_officer.name == update_data.name


def test_should_return_none_if_partial_update_an_inexistent_officer(
    db: Session,
):
    update_data = OfficerUpdate(name="change")
    updated_officer = officer_service.update(db=db, uid=9, obj=update_data)

    assert updated_officer is None


def test_should_return_true_officer_remove_with_id_existing(
    db: Session, one_officer: Officer
):
    deleted = officer_service.remove(db=db, uid=one_officer.uid)

    assert deleted


def test_should_return_false_officer_remove_with_non_existing_id(
    db: Session,
):
    deleted = officer_service.remove(db=db, uid=9)

    assert not deleted
