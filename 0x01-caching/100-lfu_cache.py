#!/usr/bin/env python3
""" a module for the LFUCache class """
from collections import defaultdict, OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """ LFU Cache class that inherits from BaseCaching """

    def __init__(self):
        """ Initialize the LFUCache class """
        super().__init__()
        self.frequency_dict = defaultdict(int)  # Frequency of access for each key
        self.use_order = OrderedDict()  # Maintains the order of usage for LRU in case of a tie

    def put(self, key, item):
        """
        Assign item to the dictionary self.cache_data with the key.
        If the number of items in self.cache_data exceeds BaseCaching.MAX_ITEMS,
        discard the least frequently used item (LFU algorithm). If there is a tie,
        discard the least recently used item among them.
        """
        if key is None or item is None:
            return

        # Update the item in the cache
        if key in self.cache_data:
            self.cache_data[key] = item
            self.frequency_dict[key] += 1
            # Update the order to mark this key as recently used
            self.use_order.move_to_end(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the LFU key (with the lowest frequency)
                min_frequency = min(self.frequency_dict.values())
                # Get all keys with the minimum frequency
                lfu_keys = [k for k in self.frequency_dict if self.frequency_dict[k] == min_frequency]
                # If there is a tie, remove the least recently used one
                if len(lfu_keys) > 1:
                    # Find the LRU among the LFU keys
                    lfu_lru_key = None
                    for k in self.use_order:
                        if k in lfu_keys:
                            lfu_lru_key = k
                            break
                else:
                    lfu_lru_key = lfu_keys[0]

                # Remove the LFU key from the cache and related tracking dicts
                if lfu_lru_key:
                    del self.cache_data[lfu_lru_key]
                    del self.frequency_dict[lfu_lru_key]
                    self.use_order.pop(lfu_lru_key)
                    print(f"DISCARD: {lfu_lru_key}")

            # Add the new key-value pair to cache
            self.cache_data[key] = item
            self.frequency_dict[key] = 1
            self.use_order[key] = None  # Add the new key to the usage order

    def get(self, key):
        """
        Return the value in self.cache_data linked to key.
        If key is None or if the key doesn't exist in self.cache_data, return None.
        """
        if key is None or key not in self.cache_data:
            return None

        # Update the frequency and usage order for this key
        self.frequency_dict[key] += 1
        self.use_order.move_to_end(key)

        return self.cache_data[key]

    def print_cache(self):
        """ Print the cache data """
        print("Current cache:")
        for key, value in self.cache_data.items():
            print(f"{key}: {value}")
