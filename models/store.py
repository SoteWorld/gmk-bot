# models/store.py

import uuid
from pydantic import BaseModel, Field
from typing import Optional

class Store(BaseModel):
    """
    Модель данных для представления магазина.
    ID будет генерироваться, так как на сайте его нет.
    """
    # Теперь ID обязателен, но будет генерироваться, если не указан (например, при парсинге, если его еще нет)
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Уникальный идентификатор магазина (генерируется).")
    name: str = Field(..., description="Название магазина.")
    address: str = Field(..., description="Полный адрес магазина.")
    opening_hours: Optional[str] = Field(None, description="Режим работы магазина (текстовое описание, например, '9:00 - 21:00').")
    phone: Optional[str] = Field(None, description="Контактный телефон магазина.", pattern=r"^\+?[0-9\s\-()]{7,20}$")
    latitude: Optional[float] = Field(None, description="Широта местоположения магазина (получается через геокодирование адреса).")
    longitude: Optional[float] = Field(None, description="Долгота местоположения магазина (получается через геокодирование адреса).")