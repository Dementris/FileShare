import uuid
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, func, ForeignKey, Table, UUID, String, CHAR
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column, Column

from fileshare.database.core import Base

files_permissions = Table(
    'files_permissions',
    Base.metadata,
    Column('file_id', ForeignKey('files.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
)


class File(Base):
    __tablename__ = 'files'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    content_type: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    size: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="files")  # noqa
    user_with_access: Mapped[List["User"]] = relationship("User", secondary="files_permissions", # noqa
                                                          back_populates="shared_files")

    temp_files: Mapped[List["TempFile"]] = relationship("TempFile", back_populates="file")

class TempFile(Base):
    __tablename__ = 'temp_files'
    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True, default=uuid.uuid4)
    temp_file_path: Mapped[str] = mapped_column(String(300), nullable=False)
    file_id: Mapped[int] = mapped_column(ForeignKey('files.id'), nullable=False)

    file: Mapped["File"] = relationship("File", back_populates="temp_files")