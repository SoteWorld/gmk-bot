from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from server.models import Product
from server.services.data_provider import DataProvider

from .dependencies import get_data_provider

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/all", response_model=List[Product])
async def list_products(data_provider: DataProvider = Depends(get_data_provider)) -> List[Product]:
    return await data_provider.list_products()

@router.get("/categories", response_model=List[str])
async def list_categories(
    data_provider: DataProvider = Depends(get_data_provider),
) -> List[str]:
    return await data_provider.list_categories()


@router.get("/category/{category}", response_model=List[Product])
async def products_by_category(
    category: str,
    data_provider: DataProvider = Depends(get_data_provider),
) -> List[Product]:
    return await data_provider.list_products_by_category(category)