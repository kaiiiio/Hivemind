"""Redis-backed episodic memory with a local fallback.

Redis is optional during development. If the client package or server is absent,
the store stays usable with an in-memory dictionary so tests and local coding do
not require paid or network services.
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

logger = logging.getLogger(__name__)

try:
    import redis
except ImportError:  # pragma: no cover - depends on local env
    redis = None


class RedisEpisodicStore:
    """T2 episodic memory store."""

    def __init__(self, redis_url: str | None = None, default_ttl_seconds: int = 7 * 24 * 3600):
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.default_ttl_seconds = default_ttl_seconds
        self._fallback: dict[str, tuple[float, dict[str, Any]]] = {}
        self.client = None

        if redis is not None:
            try:
                self.client = redis.from_url(self.redis_url, decode_responses=True)
                self.client.ping()
            except Exception as exc:  # pragma: no cover - requires redis server
                logger.warning("Redis unavailable, using in-memory episodic store: %s", exc)
                self.client = None

    def write_episode(self, ticker: str, run_date: str, episode: dict[str, Any], ttl_seconds: int | None = None) -> str:
        key = f"episode:{ticker}:{run_date}"
        ttl = ttl_seconds or self.default_ttl_seconds
        encoded = {k: json.dumps(v, default=str) for k, v in episode.items()}

        if self.client:
            self.client.hset(key, mapping=encoded)
            self.client.expire(key, ttl)
            self.client.zadd(f"ticker:recent_decisions:{ticker}", {key: int(time.time())})
            return key

        self._fallback[key] = (time.time() + ttl, episode)
        return key

    def read_recent_ticker_episodes(self, ticker: str, limit: int = 5) -> list[dict[str, Any]]:
        if self.client:
            keys = self.client.zrevrange(f"ticker:recent_decisions:{ticker}", 0, limit - 1)
            return [self._decode_hash(self.client.hgetall(key)) for key in keys]

        now = time.time()
        rows = []
        for key, (expires_at, value) in self._fallback.items():
            if key.startswith(f"episode:{ticker}:") and expires_at > now:
                rows.append((expires_at, value))
        return [value for _, value in sorted(rows, reverse=True)[:limit]]

    def append_mistake(self, agent_name: str, mistake: dict[str, Any], max_items: int = 20) -> None:
        key = f"agent:mistake_log:{agent_name}"
        if self.client:
            self.client.lpush(key, json.dumps(mistake, default=str))
            self.client.ltrim(key, 0, max_items - 1)
            return
        current = self._fallback.get(key, (time.time() + self.default_ttl_seconds, {"items": []}))[1]
        current.setdefault("items", []).insert(0, mistake)
        current["items"] = current["items"][:max_items]
        self._fallback[key] = (time.time() + self.default_ttl_seconds, current)

    def read_mistakes(self, agent_name: str, limit: int = 5) -> list[dict[str, Any]]:
        key = f"agent:mistake_log:{agent_name}"
        if self.client:
            return [json.loads(item) for item in self.client.lrange(key, 0, limit - 1)]
        current = self._fallback.get(key, (0, {"items": []}))[1]
        return current.get("items", [])[:limit]

    @staticmethod
    def _decode_hash(row: dict[str, str]) -> dict[str, Any]:
        decoded = {}
        for key, value in row.items():
            try:
                decoded[key] = json.loads(value)
            except json.JSONDecodeError:
                decoded[key] = value
        return decoded
