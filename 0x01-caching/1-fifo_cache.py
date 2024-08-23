#!/usr/bin/env python3
""" a module for the FIFOCache class """
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """ a FIFO cahce implementation that inherits from BaseCaching """

    def __init__(self):
        """ initialize the FIFO cache class """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
            sets key and item in BaseCaching self.cache_data attribute
            makes sure the cache is below its BaseCaching.MAX_ITEMS
            if not it removes first item before adding new item
            if key or item is None no operation is done
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                k, v = self.cache_data.popitem(last=False)
                print('DISCARD: {}'.format(k))
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
