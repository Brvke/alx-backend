#!/usr/bin/env python3
""" a module for the BaseCache class """
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """ a class inheriting from BaseCaching used for caching """

    def put(self, key, item):
        """
            sets key and item in BaseCaching self.cache_data attribute
            if key or item is None no operation is done
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
            gets items associated with key from self.cache_data
            if key is None or not a valid key it returns None
        """
        if key is None:
            return None

        try:
            item = self.cache_data[key]
            return item
        except KeyError:
            return None
