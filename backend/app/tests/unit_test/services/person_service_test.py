import pytest
from sqlalchemy.orm import Session
from app.models.person import Person as PersonMD
from app.schemas.person import (
    Person,
    PersonCreate,
    PersonUpdate,
)
from app.services.person_service import person_service


@pytest.fixture
def one_person(db: Session, clean_people):
    p1 = PersonMD(name="test", email="test@some.com")
    db.add(p1)
    db.commit()
    db.refresh(p1)
    return Person.model_validate(p1)


@pytest.fixture
def some_people(db: Session, clean_people):
    people = [
        PersonMD(name="test1", email="test1@some.com"),
        PersonMD(name="test2", email="test2@some.com"),
        PersonMD(name="test3", email="test3@some.com"),
    ]
    db.add_all(people)
    db.commit()
    to_return = []
    for person in people:
        to_return.append(Person.model_validate(person))
    return to_return


# Test cases


def test_should_create_person(db: Session, clean_people):
    """when an person is save, an id is assigned into the db,
    as result, the person representation should be returned as
    part of the response
    """
    input_person = PersonCreate(name="test", email="test@some.com")
    saved_person = person_service.create(db=db, obj_in=input_person)
    assert isinstance(saved_person, Person)
    assert isinstance(saved_person.uid, int)
    assert saved_person.name == input_person.name


def test_should_get_person(db: Session, one_person: Person):
    retrieved_person = person_service.get(db=db, uid=one_person.uid)

    assert isinstance(retrieved_person, Person)


def test_should_get_none_when_id_not_exist(
    db: Session,
):
    non_existing_id = 99
    retrieved_person = person_service.get(db=db, uid=non_existing_id)

    assert retrieved_person is None


def test_should_list_people(db: Session, some_people: list[Person]):
    people = person_service.get_multi(db=db)

    assert isinstance(people, list)
    assert isinstance(people[0], Person)
    assert isinstance(people[1], Person)


def test_should_allow_person_partial_update(db: Session, one_person: Person):
    update_data = PersonUpdate(email="change@test.com")
    updated_person = person_service.update(
        db=db, uid=one_person.uid, obj=update_data
    )

    assert updated_person.email == update_data.email


def test_should_return_none_if_partial_update_an_inexistent_person(
    db: Session,
):
    update_data = PersonUpdate(email="change@test.com")
    updated_person = person_service.update(db=db, uid=9, obj=update_data)

    assert updated_person is None


def test_should_return_true_person_remove_with_id_existing(
    db: Session, one_person: Person
):
    deleted = person_service.remove(db=db, uid=one_person.uid)

    assert deleted


def test_should_return_false_person_remove_with_non_existing_id(
    db: Session,
):
    deleted = person_service.remove(db=db, uid=9)

    assert not deleted
