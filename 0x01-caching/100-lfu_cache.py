#!/usr/bin/env python3
""" a module for the LFUCache class """
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """ a LFU cache implementation that inherits from BaseCaching """

    # to be used for storing values and use order
    use_dict = {}
    frequency_dict = {}
    min_LFU = 1

    def __init__(self):
        """ initalizes the LFU cache class """
        super().__init__()

    def put(self, key, item):
        """
            sets key and item in BaseCaching self.cache_data attribute
            makes sure the cache is below its BaseCaching.MAX_ITEMS
            if not it removes last item before adding new item
            if key or item is None no operation is done
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                for k, v in self.use_dict.items():
                    if v == self.MAX_ITEMS:
                        self.cache_data.pop(k)
                        print('DISCARD: {}'.format(k))
                        break
            self.LRU(key)
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
            self.LRU(key)
            return item
        except KeyError:
            return None

    def LRU(self, key):
        """ logs the use case for keys in the use_dict """

        if key is None:
            return None

        # if new key
        if key not in self.use_dict.keys():
            # if cache is full
            if len(self.use_dict) >= self.MAX_ITEMS:
                for k in self.use_dict.keys():
                    # find the LRU key
                    if self.use_dict[k] == self.MAX_ITEMS:
                        # remove LRU key
                        self.use_dict.pop(k)
                        self.use_dict[key] = 1
                        break
            else:
                # if cache isn't full simply add new key
                self.use_dict[key] = 1
            # adjust rank of all remaining keys
            for k in self.use_dict.keys():
                if k != key:
                    self.use_dict[k] += 1
        else:
            key_rank = self.use_dict[key]
            self.use_dict[key] = 1
            # change rank for all rank smaller than previous rank of key
            for k in self.use_dict.keys():
                if k != key:
                    if self.use_dict[k] < key_rank:
                        self.use_dict[k] += 1
