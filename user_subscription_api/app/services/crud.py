from typing import ClassVar, Any, Optional
from sqlalchemy.orm import Session


class CRUDBase:
    def __init__(self, db: Session, model: ClassVar):
        self.db = db
        self.model = model

    async def get(self, id: Any):
        return self.db.query(self.model).filter(self.model.id == id).first()

    async def create(self, obj: dict):
        db_obj = self.model(**obj)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    async def update(self):
        pass

    async def remove(self, id: Any):
        obj = self.db.query(self.model).get(id)
        self.db.delete(obj)
        self.db.commit()
        return obj
