#!/usr/bin/python3
""" lIFOCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache class inherit from BaseCaching
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.key_stack = []

    def __reoder_key_stack(self, key):
        """ Reorder the key stack
        """
        key_matching_idx = -1
        latest_key = self.key_stack[-1]
        for idx, value in enumerate(self.key_stack):
            if key == value:
                key_matching_idx = idx
        self.key_stack[key_matching_idx] = latest_key
        self.key_stack[-1] = key

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if key not in self.cache_data:
            self.key_stack.append(key)
        else:
            self.__reoder_key_stack(key)

        self.cache_data.update({key: item})

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            last_in = self.key_stack[-2]
            self.key_stack.remove(last_in)
            self.cache_data.pop(last_in)
            print("DISCARD: {}".format(last_in))

    def get(self, key):
        """ Get an item by key
        """
        if key is None:
            return None
        elif (key in self.cache_data.keys()) is not True:
            return None
        else:
            return self.cache_data[key]
