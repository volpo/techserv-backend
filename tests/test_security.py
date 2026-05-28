import uuid

from app.core.security import UserRole, create_access_token, decode_jwt, hash_password, verify_password


def test_jwt_roundtrip():
    user_id = uuid.uuid4()
    token = create_access_token(user_id, "test@techserv.local", UserRole.SUPERVISOR)
    payload = decode_jwt(token)
    assert payload.sub == str(user_id)
    assert payload.role == UserRole.SUPERVISOR.value


def test_password_hash():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed)
    assert not verify_password("wrong", hashed)
