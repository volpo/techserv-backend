import uuid

from app.core.security import UserRole, create_test_token, decode_supabase_jwt


def test_jwt_roundtrip():
    user_id = uuid.uuid4()
    token = create_test_token(user_id, role=UserRole.SUPERVISOR)
    payload = decode_supabase_jwt(token)
    assert payload.sub == str(user_id)
    assert payload.role == UserRole.SUPERVISOR
