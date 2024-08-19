#!/usr/bin/env python3
""" a module for the server class """
import csv
import math
from typing import List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def index_range(self, page: int, page_size: int) -> tuple:
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

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
            Args:
                page: a 1 indexed variable for the current page
                page_size: a size for the amount in a single page
            Return:
                - an empty list if arguments out of range
                - an assertion error if invalid arguments
                - or a list of rows with size @page_size
        """

        # assert arguments are positive integers
        assert type(page) == int
        assert type(page_size) == int
        assert page > 0
        assert page_size > 0

        # get the start and end indexes
        out_range = self.index_range(page, page_size)

        output = []
        # open the file
        with open('Popular_Baby_Names.csv', newline='') as f:
            # create a reader object to read the csv file
            reader = csv.reader(f)

            # convert the reader object to list so access row by index
            input = list(reader)

            # delete the first row only from reader object not from file
            # so it donesn't skew search since it is only a header
            del input[0]

            # check if given range is within range of file
            if out_range[1] > len(input):
                return []

            # appen rows to list and return list
            for i in range(out_range[0], out_range[1]):
                output.append(input[i])

        return output

    def get_hyper(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
            Args:
                page: a 1 indexed variable for the current page
                page_size: a size for the amount in a single page
            Returns:
                a dict with the following format
                {
                    page_size: the length of the returned dataset page
                    page: the current page number
                    data: the dataset page,
                          equivalent to return from get_page
                    next_page: number of the next page,
                               None if no next page
                    prev_page: number of the previous page,
                               None if no previous page
                    total_pages: the total number of pages
                                 in the dataset as an integer
                }
        """

        out_dict = {
                    "page_size": page_size,
                    "page": page,
                    "data": self.get_page(page, page_size)
                   }

        with open('Popular_Baby_Names.csv', newline='') as f:
            # create a reader object to read the csv file
            reader = csv.reader(f)

            # convert the reader object to list so access row by index
            input = list(reader)

            # delete the first row only from reader object not from file
            # so it doesn't skew search since it is only a header
            del input[0]

            total_pages = math.ceil(len(input) / page_size)

            if page >= total_pages:
                out_dict["next_page"] = None
            else:
                out_dict["next_page"] = page + 1

            if page <= 1:
                out_dict["prev_page"] = None
            else:
                out_dict["prev_page"] = page - 1

        out_dict["total_pages"] = total_pages

        return out_dict
