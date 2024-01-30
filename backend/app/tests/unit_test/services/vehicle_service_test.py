import pytest
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle as VehicleMD
from app.schemas.vehicle import (
    Vehicle,
    VehicleCreate,
    VehicleUpdate,
)
from app.services.vehicle_service import vehicle_service


@pytest.fixture
def clean_vehicles(db: Session):
    yield None
    db.query(VehicleMD).delete()


@pytest.fixture
def one_vehicle(db: Session, clean_vehicles):
    p1 = VehicleMD(plate="abc123", brand="one", color="blue", owner_id=1)
    db.add(p1)
    db.commit()
    db.refresh(p1)
    return Vehicle.model_validate(p1)


@pytest.fixture
def some_vehicles(db: Session, clean_vehicles):
    vehicles = [
        VehicleMD(plate="abc123", brand="one", color="red", owner_id=1),
        VehicleMD(plate="abc456", brand="two", color="green", owner_id=1),
        VehicleMD(plate="abc789", brand="three", color="blue", owner_id=1),
    ]
    db.add_all(vehicles)
    db.commit()
    to_return = []
    for vehicle in vehicles:
        to_return.append(Vehicle.model_validate(vehicle))
    return to_return


# Test cases


def test_should_create_vehicle(db: Session, clean_vehicles):
    """when an vehicle is save, an id is assigned into the db,
    as result, the vehicle representation should be returned as
    part of the response
    """
    input_vehicle = VehicleCreate(
        plate="abc123", brand="one", color="blue", owner_id=1
    )
    saved_vehicle = vehicle_service.create(db=db, obj_in=input_vehicle)
    assert isinstance(saved_vehicle, Vehicle)
    assert isinstance(saved_vehicle.uid, int)
    assert saved_vehicle.plate == input_vehicle.plate


def test_should_get_vehicle(db: Session, one_vehicle: Vehicle):
    retrieved_vehicle = vehicle_service.get(db=db, uid=one_vehicle.uid)

    assert isinstance(retrieved_vehicle, Vehicle)


def test_should_get_none_when_id_not_exist(
    db: Session,
):
    non_existing_id = 99
    retrieved_vehicle = vehicle_service.get(db=db, uid=non_existing_id)

    assert retrieved_vehicle is None


def test_should_list_vehicles(db: Session, some_vehicles: list[Vehicle]):
    vehicles = vehicle_service.get_multi(db=db)

    assert isinstance(vehicles, list)
    assert isinstance(vehicles[0], Vehicle)
    assert isinstance(vehicles[1], Vehicle)


def test_should_allow_vehicle_partial_update(
    db: Session, one_vehicle: Vehicle
):
    update_data = VehicleUpdate(plate="abc456")
    updated_vehicle = vehicle_service.update(
        db=db, uid=one_vehicle.uid, obj=update_data
    )

    assert updated_vehicle.plate == update_data.plate


def test_should_return_none_if_partial_update_an_inexistent_vehicle(
    db: Session,
):
    update_data = VehicleUpdate(plate="abc456")
    updated_vehicle = vehicle_service.update(db=db, uid=9, obj=update_data)

    assert updated_vehicle is None


def test_should_return_true_vehicle_remove_with_id_existing(
    db: Session, one_vehicle: Vehicle
):
    deleted = vehicle_service.remove(db=db, uid=one_vehicle.uid)

    assert deleted


def test_should_return_false_vehicle_remove_with_non_existing_id(
    db: Session,
):
    deleted = vehicle_service.remove(db=db, uid=9)

    assert not deleted
