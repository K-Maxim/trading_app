from fastapi_users import FastAPIUsers

from fastapi import FastAPI

from auth.base_config import auth_backend

from auth.manager import get_user_manager
from auth.model import User
from auth.schemas import UserRead, UserCreate
from operations.router import router as router_operation

app = FastAPI(
    title="Trading app"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)