#!/usr/bin/env python3
"""
Exercise Redis Module
"""
import redis
from uuid import uuid4
from typing import Union


class Cache:
    """Cache abstraction class for the redis module."""
    def __init__(self):
        """Initialize the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Create a store for the cache."""
        id = str(uuid4())
        self._redis.set(id, data)
        return id
