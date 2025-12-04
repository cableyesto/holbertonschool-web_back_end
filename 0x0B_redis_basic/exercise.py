#!/usr/bin/env python3
"""
Exercise Redis Module
"""
import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Count calls decorators."""
    @wraps(method)
    def wrapper(self, *args, **kwds):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Call inputs and outputs decorators."""
    @wraps(method)
    def wrapper(self, *args):
        self._redis.rpush("{}:inputs".format(method.__qualname__), str(args))
        res = method(self, *args)
        self._redis.rpush("{}:outputs".format(method.__qualname__), res)
        return res
    return wrapper


class Cache:
    """Cache abstraction class for the redis module."""
    def __init__(self):
        """Initialize the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
