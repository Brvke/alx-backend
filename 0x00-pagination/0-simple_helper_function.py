#!/usr/bin/env python3
""" a module for the index_range function """


def index_range(page: int, page_size: int) -> tuple:
    """
        Args:
            page: a 1 indexed variable for the current page
            page_size: a size for the amount in a single page
        Returns:
            a tuple for the start and end index of values
            to be displayed on the current page
    """

    if page == 1:
        return (0, page_size)

    start = (page - 1) * page_size
    end = page * page_size

    return (start, end)
