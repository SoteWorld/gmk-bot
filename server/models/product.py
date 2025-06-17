import uuid
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional


class Product(BaseModel):
    """Модель данных для представления нового продукта."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Уникальный идентификатор продукта (генерируется).")
    name: str = Field(..., description="Название продукта.")
    image: Optional[str] = Field(None, description="URL картинки продукта.")
    expiration_date: Optional[str] = Field(None, description="Срок годности продукта.")
    ingredients: Optional[str] = Field(None, description="Состав продукта.")
    category: Optional[str] = Field(None, description="Тип продукта (например, новинка, пельмени и т.д.).")
