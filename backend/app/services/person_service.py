from sqlalchemy.orm import Session
from app.models.person import Person as PersonMD
from app.schemas.person import Person, PersonCreate, PersonUpdate

from fastapi.encoders import jsonable_encoder


class PersonService:
    # def __init__(self, repository):
    #     self._repository = repository
    def get(self, db: Session, uid: int) -> Person | None:
        item = db.query(PersonMD).filter(PersonMD.uid == uid).one_or_none()
        if item is None:
            return None
        else:
            return Person.model_validate(item)

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        items = db.query(PersonMD).offset(skip).limit(limit).all()
        people = []
        for item in items:
            people.append(Person.model_validate(item))
        return people

    def create(self, db: Session, *, obj_in: PersonCreate) -> Person:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = PersonMD(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return Person.model_validate(db_obj)

    def update(
        self, db: Session, *, uid: int, obj: PersonUpdate
    ) -> Person | None:
        item = db.query(PersonMD).filter(PersonMD.uid == uid).one_or_none()
        if item is None:
            return None
        else:
            # item.
            # person = Person.model_validate(item)
            obj_db = jsonable_encoder(item)
            update_data = obj.model_dump(exclude_unset=True)
            for field in obj_db:
                if field in update_data:
                    setattr(item, field, update_data[field])
            db.add(item)
            db.commit()
            db.refresh(item)
            return item

    def remove(self, db: Session, *, uid: int) -> Person | None:
        obj = db.query(PersonMD).get(uid)
        if obj is None:
            return None
        else:
            db.delete(obj)
            db.commit()
            return obj


person_service = PersonService()
