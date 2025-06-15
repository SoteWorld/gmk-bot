from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from server.models import Product
from server.services.data_provider import DataProvider

from .dependencies import get_data_provider

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/new", response_model=List[Product])
async def list_products(data_provider: DataProvider = Depends(get_data_provider)) -> List[Product]:
    return await data_provider.list_products()
