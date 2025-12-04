#!/usr/bin/env python3
"""
Exercise Redis Module
"""
import redis
from uuid import uuid4
from typing import Union, Callable


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

    def get(self, key: str, fn: Callable = None):
        """Retrieve data from redis."""
        if not key:
            return None

        res = self._redis.get(key)
        if not res:
            return None
        if not fn:
            return res
        else:
            return fn(res)

    def get_str(self, key: str):
        """Retrieve string from redis."""
        if not key:
            return None

        def fn(x):
            """Lambda function"""
            return str(x)
        self.get(key, fn)

    def get_int(self, key: str):
        """Retrieve integer from redis."""
        if not key:
            return None

        def fn(x):
            """Lambda function"""
            return int(x)
        self.get(key, fn)
