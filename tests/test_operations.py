import datetime

from httpx import AsyncClient
from conftest import client, async_session_maker
from sqlalchemy import insert, select, delete, update
from auth.model import role, users
from operations.models import operation


def test_add_specific_operations():
    response = client.post("/operations", json={
        "quantity": "25.5",
        "figi": "figi_CODE",
        "instrument_type": "bond",
        "date": "2023-04-28 17:25:08.768000",
        "type": "Выплата купонов",
    })

    assert response.status_code == 200


def test_get_specific_operations():
    response = client.get("/operations", params={
        "operation_type": "Выплата купонов",
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 1

# ДОРАБОТАТЬ
# async def test_put_specific_operations(operation_id: int = 1):
#     response = client.put(f"/operations/{operation_id}")
#     # data = {
#     #     "quantity": "25.5",
#     #     "figi": "figi_CODE",
#     #     "instrument_type": "bond",
#     #     "date": datetime.now(),
#     #     "type": "Покупка акций"
#     # }
#     async with async_session_maker() as session:
#         stmt = update(operation).where(operation.c.id == operation_id).values(type="Покупка акций")
#         await session.execute(stmt)
#         await session.commit()
#
#         assert response.status_code == 200
#         assert response.json()["status"] == "success"


async def test_delete_specific_operations(operation_id: int = 1):
    async with async_session_maker() as session:
        response = client.delete(f"/operations/{operation_id}")
        stmt = delete(operation).where(operation.c.id == operation_id)
        await session.execute(stmt)
        await session.commit()

        assert response.status_code == 200
        assert response.json()["status"] == "success"
