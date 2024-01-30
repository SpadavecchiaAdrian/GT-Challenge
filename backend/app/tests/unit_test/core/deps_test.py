import pytest
from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from app.schemas.officer import Officer
from app.models.officer import Officer as OfficerMD
from app.core.security import create_access_token
from app.core.deps import (
    # get_database,
    get_current_user,
)


@pytest.fixture
def generate_token(one_officer: Officer) -> str:
    return create_access_token(one_officer.uid)


def test_should_return_the_user_owner_of_token(
    db: Session, generate_token: str
):
    token_user = get_current_user(db=db, token=generate_token)
    assert isinstance(token_user, Officer)


def test_should_rise_forbidden_exception_if_bad_token(db: Session):
    with pytest.raises(HTTPException) as e:
        get_current_user(db=db, token="fake token")

    assert e.value.status_code == status.HTTP_403_FORBIDDEN


def test_should_rise_not_found_exception_if_user_not_found(db: Session):
    fake_token = create_access_token(subject=9)
    with pytest.raises(HTTPException) as e:
        get_current_user(db=db, token=fake_token)

    assert e.value.status_code == status.HTTP_404_NOT_FOUND
