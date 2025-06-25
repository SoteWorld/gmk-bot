from __future__ import annotations

import json
from typing import Any, List, Optional

from server.constants import REDIS_JSON_TTL

import redis.asyncio as redis


class BaseRedisRepository:
    """Общий класс для работы с Redis."""

    def __init__(self, url: str = "redis://localhost", *, decode_responses: bool = True) -> None:
        self._redis = redis.from_url(url, decode_responses=decode_responses)

    async def close(self) -> None:
        await self._redis.close()

    async def flush(self) -> None:
        """Очищает текущую БД Redis от абсолютно всех данных."""
        await self._redis.flushdb()

    async def _delete_by_pattern(self, pattern: str) -> None:
        """Удаляет из Redis все ключи, подходящие под указанный шаблон."""
        keys = await self._scan_keys(pattern)
        if keys:
            await self._redis.delete(*keys)

    # -------------------- вспомогательные методы --------------------
    async def _set_json(self, key: str, value: Any, ttl: int | None = REDIS_JSON_TTL) -> None:
        data = json.dumps(value)
        await self._redis.set(key, data, ex=ttl)

    async def _get_json(self, key: str) -> Optional[Any]:
        data = await self._redis.get(key)
        return json.loads(data) if data else None

    async def _delete(self, key: str) -> None:
        await self._redis.delete(key)

    async def _scan_keys(self, pattern: str) -> List[str]:
        cursor = 0
        keys: List[str] = []
        while True:
            cursor, batch = await self._redis.scan(cursor=cursor, match=pattern)
            keys.extend(batch)
            if cursor == 0:
                break
        return keys
