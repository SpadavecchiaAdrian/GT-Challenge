from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.models.vehicle import Vehicle


class Person(Base):
    __tablename__ = "people"

    uid: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    email: Mapped[str] = mapped_column(index=True)
    name: Mapped[str]
    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="owner")
