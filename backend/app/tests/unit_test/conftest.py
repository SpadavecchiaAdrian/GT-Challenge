import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Generator
from app.models.officer import Officer as OfficerMD
from app.models.vehicle import Vehicle as VehicleMD
from app.models.person import Person as PersonMD
from app.models.infraction import Infraction as InfractionMD
from app.db.database import SessionLocal
from app.main import app
from app.core.security import get_password_hash
from app.schemas.officer import Officer


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def clean_officers(db: Session):
    yield None
    db.query(OfficerMD).delete()


@pytest.fixture
def one_officer(db: Session, clean_officers):
    p1 = OfficerMD(name="test", hashed_password=get_password_hash("1234"))
    db.add(p1)
    db.commit()
    db.refresh(p1)
    return Officer.model_validate(p1)


@pytest.fixture(scope="function")
def clean_vehicles(db: Session):
    yield None
    db.query(VehicleMD).delete()


@pytest.fixture(scope="function")
def clean_people(db: Session):
    yield None
    db.query(PersonMD).delete()


@pytest.fixture(scope="function")
def clean_infractions(db: Session):
    yield None
    db.query(InfractionMD).delete()
    db.query(VehicleMD).delete()
