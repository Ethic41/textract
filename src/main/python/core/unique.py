# Author: Dahir Muhammad Dahir
# Date: 21st-05-2019 10:49 AM

from itertools import product
from string import ascii_uppercase as letters


class Unique:
    def __init__(self):
        self.start = 1
        self.chain = None

    def make_chain(self):
        self.chain = product(letters, repeat=self.start)
        self.start += 1

    def get_unique_key(self):
        try:
            return "".join(self.chain.__next__())
        except StopIteration:
            self.make_chain()
            return "".join(self.chain.__next__())
