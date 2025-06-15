from __future__ import annotations

from functools import lru_cache

from server.services.data_provider import DataProvider

@lru_cache
def get_data_provider() -> DataProvider:
    return DataProvider()