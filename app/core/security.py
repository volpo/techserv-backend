import uuid
from datetime import UTC, datetime
from enum import StrEnum

from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings


class UserRole(StrEnum):
    CLIENTE = "cliente"
    TECNICO = "tecnico"
    SUPERVISOR = "supervisor"
    ADMINISTRADOR = "administrador"
    AREA_ADMINISTRATIVA = "area_administrativa"


class TokenPayload(BaseModel):
    sub: str
    email: str | None = None
    role: str | None = None
    exp: int | None = None


def decode_supabase_jwt(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=[settings.jwt_algorithm],
            options={"verify_aud": False},
        )
    except JWTError as exc:
        raise ValueError("Invalid or expired token") from exc

    sub = payload.get("sub")
    if not sub:
        raise ValueError("Token missing subject")

    return TokenPayload(
        sub=sub,
        email=payload.get("email"),
        role=payload.get("role") or payload.get("user_metadata", {}).get("role"),
        exp=payload.get("exp"),
    )


def create_test_token(
    user_id: uuid.UUID,
    email: str = "test@techserv.local",
    role: UserRole = UserRole.ADMINISTRADOR,
) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role.value,
        "iat": int(now.timestamp()),
        "exp": int(now.timestamp()) + 3600,
    }
    return jwt.encode(payload, settings.supabase_jwt_secret, algorithm=settings.jwt_algorithm)
