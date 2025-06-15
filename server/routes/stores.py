from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, Query

from server.models import StoreWithDistance
from server.services.data_provider import DataProvider

from .dependencies import get_data_provider

router = APIRouter(prefix="/stores", tags=["stores"])

@router.get("/nearby", response_model=List[StoreWithDistance])
async def list_nearby_stores(
    lat: float = Query(..., description="User latitude"),
    lon: float = Query(..., description="User longitude"),
    limit: int = Query(5, ge=1, description="Limit number of stores"),
    data_provider: DataProvider = Depends(get_data_provider),
) -> List[StoreWithDistance]:
    # https://9b15cf90cd3ef5b93a7c5ec67d7f734d.serveo.net/stores/nearby?lat=0&lon=0
    stores = await data_provider.list_stores_sorted((lat, lon))
    return stores[:limit]