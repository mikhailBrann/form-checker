from sqlalchemy import String, Integer, Column, Enum
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum
from passlib.context import CryptContext

from .base import Base
from .enum.user_role import UserRole


class User(Base):
    __tablename__ = "users"
    _pwd_context = CryptContext(
        schemes=["bcrypt"], 
        deprecated="auto"
    )

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(50), 
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100), 
        unique=True, 
        nullable=False
    )
    _password: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), 
        default=UserRole.user, 
        nullable=False
    )

    def verify_password(self, plain_password: str) -> bool:
        return self._pwd_context.verify(plain_password, self._password)

    def set_password(self, plain_password: str) -> None:
        self._password = self._pwd_context.hash(plain_password)

    @property
    def password(self) -> str:
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, plain_password: str) -> None:
        self.set_password(plain_password)

    