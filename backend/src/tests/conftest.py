from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from fileshare.auth.routes import auth_router, user_router
from httpx import ASGITransport, AsyncClient

from fileshare.database.core import sessionmanager, get_db


@pytest.fixture
def app():

    def override_db():
        sessionmanager.init("sqlite+aiosqlite:///:memory")
        async with sessionmanager.session() as session:
            yield session

    test_app = FastAPI(debug=True, root_path="/api/v1")

    test_app.dependency_overrides[get_db] = override_db # noqa

    test_app.include_router(auth_router, prefix="/auth")
    test_app.include_router(user_router, prefix="/user")
    return test_app

@pytest.fixture
async def async_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client