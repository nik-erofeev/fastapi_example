from passlib.context import CryptContext

from app.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_user_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(user: User, password: str) -> User | None:
    if user and verify_user_password(password, user.password):
        return user
