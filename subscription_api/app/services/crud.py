from typing import Any, ClassVar, TypeVar

from sqlalchemy.orm import Session

from app.db.base_class import TimeStampBase

ModelType = TypeVar("ModelType", bound=TimeStampBase)


class CRUDBase:

    def __init__(self, db: Session, model: ClassVar):
        self.db = db
        self.model = model

    async def get(self, _id: Any):
        return await self.db.get(self.model, _id)

    async def create(self, obj: dict):
        db_obj = self.model(**obj)
        self.db.add(db_obj)
        await self.db.commit()
        return db_obj

    async def update(self, db_obj: ModelType, update_data: dict):
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        await self.db.commit()
        # self.db.refresh(db_obj)
        return db_obj

    async def remove(self, _id: Any):
        db_obj = self.db.query(self.model).get(_id)
        self.db.delete(db_obj)
        self.db.commit()
        return db_obj
