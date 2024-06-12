import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost:5432/feedback_db"

# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Create a configured "Session" class for testing
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Override the get_db dependency to use the testing database
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# Create the tables for testing
@pytest.fixture(scope="module", autouse=True)
async def setup_and_teardown():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        # Drop tables
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_feedback():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/feedback",
            json={"score": 5},
        )
    assert response.status_code == 200
    assert response.json() == {"message": "Feedback submitted successfully"}

