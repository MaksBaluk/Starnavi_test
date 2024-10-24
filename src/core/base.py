from sqlalchemy import Integer, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Annotated
from datetime import datetime
from fastapi import HTTPException

created_time = Annotated[datetime, mapped_column(default=datetime.utcnow())]
updated_time = Annotated[
    datetime, mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)]


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)


class BaseService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, model: Base) -> None:
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

    def get_or_404(self, model: Base, model_id: int):
        obj = self.db.query(model).filter(model.id == model_id).first()
        if obj is None:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        return obj

    def delete(self, model: Base) -> None:
        self.db.delete(model)
        self.db.commit()
