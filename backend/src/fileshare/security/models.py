from lib2to3.btm_utils import tokens

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fileshare.auth.models import User
from fileshare.database.core import Base

class Token(Base):
    __tablename__ = 'token'
    id: Mapped[int] = mapped_column(index=True, auto_increment=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped[User] = relationship(back_populates=tokens)