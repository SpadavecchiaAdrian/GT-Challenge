from app.db.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.person import Person


class Vehicle(Base):
    __tablename__ = "vehicles"

    uid: Mapped[int] = mapped_column("id", primary_key=True, index=True)

    plate: Mapped[str] = mapped_column(index=True)
    brand: Mapped[str]
    color: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey("people.id"))
    owner: Mapped[Person] = relationship(back_populates="vehicles")
