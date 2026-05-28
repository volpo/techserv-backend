import os

os.environ.setdefault("DEBUG", "false")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-pytest-only")

import uuid
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base, get_db
from app.core.security import UserRole, create_access_token, hash_password
from app.main import app
from app.models import Company, User

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def seeded_session(db_session: AsyncSession) -> AsyncSession:
    company = Company(id=uuid.uuid4(), name="TechServ Demo")
    admin = User(
        id=uuid.uuid4(),
        email="admin@techserv.local",
        full_name="Admin User",
        role=UserRole.ADMINISTRADOR,
        company_id=company.id,
        password_hash=hash_password("admin123"),
    )
    db_session.add(company)
    db_session.add(admin)
    await db_session.commit()
    db_session.info["admin"] = admin
    db_session.info["company"] = company
    return db_session


@pytest_asyncio.fixture
async def client(seeded_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield seeded_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(seeded_session: AsyncSession) -> str:
    admin: User = seeded_session.info["admin"]
    return create_access_token(admin.id, admin.email, UserRole(admin.role))
