import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select

from auth.model import role, users
from conftest import client, async_session_maker
from operations.utils import as_dict


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name="admin", permission=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        assert as_dict(result) == [{'id': 1, 'name': 'admin', 'permission': None}], "Роль не добавилась"


async def test_register_positive(ac: AsyncClient):
    data = {
        "email": "string",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 1
    }

    response = await ac.post("/auth/register", json=data)

    assert response.status_code == 201, "Пользователь не создался"


async def test_register_negative(ac: AsyncClient):
    data = {
        "email": "",
        "password": "",
        "is_active": None,
        "is_superuser": None,
        "is_verified": None,
        "username": "",
        "role_id": None
    }

    response = await ac.post("/auth/register", json=data)

    assert response.status_code == 422
