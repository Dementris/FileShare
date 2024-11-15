from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, UUID, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fileshare.database.core import Base

class Token(Base):
    __tablename__ = 'token'
    id: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = relationship(back_populates="tokens") # noqa