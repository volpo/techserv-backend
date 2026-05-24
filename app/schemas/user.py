import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.security import UserRole


class UserBase(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    full_name: str = Field(min_length=1, max_length=255)
    role: UserRole
    company_id: uuid.UUID | None = None
    phone: str | None = None


class UserCreate(UserBase):
    id: uuid.UUID


class UserUpdate(BaseModel):
    full_name: str | None = None
    role: UserRole | None = None
    phone: str | None = None
    is_active: bool | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
    created_at: datetime


class MeResponse(UserRead):
    pass
