from itertools import count, product
from string import ascii_uppercase as letters


class Infinite:
    def __init__(self):
        self.start = 1
        self.chain = None

    def make_chain(self):
        chain = product(letters, repeat=self.start)
        self.chain = chain
        self.start += 1

    def get_unique_key(self):
        try:
            return "".join(self.chain.__next__())
        except StopIteration:
            self.make_chain()
            return "".join(self.chain.__next__())


inf = Infinite()
inf.make_chain()
print(inf.get_unique_key())
print(inf.get_unique_key())
print(inf.get_unique_key())
print(inf.get_unique_key())
print(inf.get_unique_key())

# for i in range(10):
#    print(inf.get_unique_key())

"""
def infinite_seq():
    counter = count(1)
    letter = "ABCDEFGHIJ"
    for i in counter:
        if i > 3:
            break
        for j in product(letter, repeat=i):
            print("".join(j))


infinite_seq()
"""
