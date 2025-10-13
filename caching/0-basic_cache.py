#!/usr/bin/python3
""" BasicCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """ Basic Cache class inherit from BaseCaching
    """

    # def __init__(self):
    #     """ Initialize
    #     """
    #     super().__init__(self)

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return
        else:
            self.cache_data.update({key: item})

    def get(self, key):
        """ Get an item by key
        """
        if key is None:
            return
        elif (key in self.cache_data.keys()) is not True:
            return
        else:
            return self.cache_data[key]
