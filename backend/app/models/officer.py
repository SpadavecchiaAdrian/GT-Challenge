from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.models.infraction import Infraction


class Officer(Base):
    __tablename__ = "officers"

    uid: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    name: Mapped[str]
    # infractions: Mapped[Infraction] = relationship(back_populates="officer")
