from app.db.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.vehicle import Vehicle


class Infraction(Base):
    __tablename__ = "infractions"

    uid: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    vehicle: Mapped[Vehicle] = relationship()
    timestamp: Mapped[int]
    comments: Mapped[str]
