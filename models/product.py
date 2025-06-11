import uuid
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class Product(BaseModel):
    """
    Модель данных для представления нового продукта.
    ID будет генерироваться, так как на сайте его нет.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Уникальный идентификатор продукта (генерируется).")
    name: str = Field(..., description="Название продукта.")
    description: Optional[str] = Field(None, description="Описание продукта.")
    expiration_date: Optional[date] = Field(None, description="Срок годности продукта.")
    ingredients: Optional[str] = Field(None, description="Состав продукта.")
