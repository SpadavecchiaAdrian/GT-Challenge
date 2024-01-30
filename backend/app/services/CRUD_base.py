from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import Base

from fastapi.encoders import jsonable_encoder

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(
    Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(self, model: Type[ModelType], schema: Type[SchemaType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete
        (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.schema = schema

    def get(self, db: Session, uid: int) -> SchemaType | None:
        item = db.query(self.model).filter(self.model.uid == uid).one_or_none()
        if item is None:
            return None
        else:
            return self.schema.model_validate(item)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[SchemaType]:
        items = db.query(self.model).offset(skip).limit(limit).all()
        people = []
        for item in items:
            people.append(self.schema.model_validate(item))
        return people

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> SchemaType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return self.schema.model_validate(db_obj)

    def update(
        self, db: Session, *, uid: int, obj: UpdateSchemaType
    ) -> SchemaType | None:
        item = db.query(self.model).filter(self.model.uid == uid).one_or_none()
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

    def remove(self, db: Session, *, uid: int) -> SchemaType | None:
        obj = db.query(self.model).filter(self.model.uid == uid).one_or_none()
        if obj is None:
            return None
        else:
            db.delete(obj)
            db.commit()
            return obj
