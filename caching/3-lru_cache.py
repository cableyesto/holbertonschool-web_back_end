#!/usr/bin/python3
""" LRUCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache class inherit from BaseCaching
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.key_weight_stack = []

    def __push_last_modified_at_top_key_weight_stack(self, key):
        """ Reorder the key stack
        """
        get_item = {}
        for idx, value in enumerate(self.key_weight_stack):
            if key == value['key_value']:
                value['weight'] += 1
                get_item = value
        self.key_weight_stack.remove(get_item)
        self.key_weight_stack.append(get_item)

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if key not in self.cache_data:
            self.key_weight_stack.append({"key_value": key, "weight": 1})
        else:
            self.__push_last_modified_at_top_key_weight_stack(key)

        # print(self.key_weight_stack)
        self.cache_data.update({key: item})

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first_in = self.key_weight_stack[0]
            self.key_weight_stack.remove(first_in)
            self.cache_data.pop(first_in["key_value"])
            print("DISCARD: {}".format(first_in["key_value"]))

    def get(self, key):
        """ Get an item by key
        """
        if key is None:
            return None
        elif (key in self.cache_data.keys()) is not True:
            return None
        else:
            self.__push_last_modified_at_top_key_weight_stack(key)
            return self.cache_data[key]
