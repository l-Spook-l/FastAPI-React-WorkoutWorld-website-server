# Это куки и JWT
from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from fastapi_users import FastAPIUsers
from src.config import SECRET_KEY
from .manager import get_user_manager
from .models import User

# настройка куки
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


# JWT
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=2592000)


# авторизация по JWT
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# получаем пользователя
current_user = fastapi_users.current_user()
