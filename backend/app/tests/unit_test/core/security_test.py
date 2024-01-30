from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.security import (
    ALGORITHM,
    create_access_token,
    decode_access_token,
    pwd_context,
    verify_password,
    get_password_hash,
)
from app.schemas.token import TokenPayload


class TestCreateToken:
    def test_should_create_access_token(self):
        uid = str(9)
        token = create_access_token(subject=uid)
        token_decode = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        assert isinstance(token, str)
        assert token_decode["sub"] == uid
        assert isinstance(token_decode["exp"], int)

    def test_should_create_access_token_with_custom_deltatime(self):
        uid = 9
        expire_delta = timedelta(minutes=5)
        token = create_access_token(subject=uid, expires_delta=expire_delta)
        assert isinstance(token, str)


def test_should_decode_access_token():
    uid = 9

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(uid)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM
    )
    token_decode = decode_access_token(encoded_jwt)
    assert isinstance(token_decode, TokenPayload)
    assert token_decode.sub == uid


class TestVerifyPassword:
    def test_should_return_true_if_verify_password(self):
        password = "testing"
        hashed_pass = pwd_context.hash(password)
        verification = verify_password(
            plain_password=password, hashed_password=hashed_pass
        )
        assert verification

    def test_should_return_false_if_password_dont_verify(self):
        password = "testing"
        hashed_pass = pwd_context.hash(password)
        verification = verify_password(
            plain_password="NotTheCorrectOne", hashed_password=hashed_pass
        )
        assert not verification


def test_should_hash_a_password():
    password = "testing"
    hashed_pass = get_password_hash(password)
    assert pwd_context.verify(secret=password, hash=hashed_pass)
