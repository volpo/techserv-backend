"""Crear usuario administrador inicial. Uso: python -m scripts.seed_admin"""

import asyncio
import uuid

from sqlalchemy import select

from app.core.database import async_session_factory
from app.core.security import UserRole, hash_password
from app.models import Company, User

ADMIN_EMAIL = "admin@techserv.local"
ADMIN_PASSWORD = "admin123"
ADMIN_NAME = "Administrador"


async def main() -> None:
    async with async_session_factory() as session:
        existing = await session.execute(select(User).where(User.email == ADMIN_EMAIL))
        if existing.scalar_one_or_none():
            print(f"Usuario {ADMIN_EMAIL} ya existe.")
            return

        company = Company(id=uuid.uuid4(), name="TechServ Demo")
        admin = User(
            id=uuid.uuid4(),
            email=ADMIN_EMAIL,
            full_name=ADMIN_NAME,
            role=UserRole.ADMINISTRADOR,
            company_id=company.id,
            password_hash=hash_password(ADMIN_PASSWORD),
            is_active=True,
        )
        session.add(company)
        session.add(admin)
        await session.commit()
        print(f"Admin creado: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(main())
