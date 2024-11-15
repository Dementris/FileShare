from datetime import datetime
from typing import List

from sqlalchemy import CHAR, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .constants import Roles

from fileshare.database.core import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(255),unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Roles] = mapped_column(CHAR(1), nullable=False, default=Roles.USER)
    # Set default values for created_at and updated_at
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    disabled: Mapped[bool] = mapped_column(default=False, nullable=False)

    tokens: Mapped[List["Token"]] = relationship("Token", back_populates="user")  # noqa
    files: Mapped[List["File"]] = relationship("File", back_populates="owner")  # noqa

    shared_files: Mapped[List["File"]] = relationship("File", secondary="files_permissions", # noqa
                                                      back_populates="user_with_access")
