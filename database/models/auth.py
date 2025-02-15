from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import BigInteger, String, Column, ForeignKey, Integer
from .base import Base
from .user import User


class Auth(Base):
    __tablename__ = 'authentifications'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    key: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship("User")