#!/usr/bin/python3
""" FIFOCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache class inherit from BaseCaching
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return
        else:
            self.cache_data.update({key: item})

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_key = list(self.cache_data.keys())[0]
            self.cache_data.pop(first_key)
            print("DISCARD: {}".format(first_key))

    def get(self, key):
        """ Get an item by key
        """
        if key is None:
            return None
        elif (key in self.cache_data.keys()) is not True:
            return None
        else:
            return self.cache_data[key]
