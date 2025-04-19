from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist

from src.core.database.models import Users


# 使用 passlib 的 CryptContext 来处理密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 验证明文密码是否与哈希密码匹配
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 获取密码的哈希值
def get_password_hash(password):
    return pwd_context.hash(password)


# # 根据用户名从数据库中获取用户
# async def get_user(username: str):
#     return await UserDatabaseSchema.from_queryset_single(Users.get(username=username))


async def validate_user(user: OAuth2PasswordRequestForm = Depends()):
    try:
        db_user = await Users.get(username=user.username)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return db_user