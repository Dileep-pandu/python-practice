import random


class RandomizedSet:
    # Time: O(1) average per call, Space: O(n)

    def __init__(self):
        self.values = []        # random.choice needs a list
        self.index_of = {}      # value -> its position in self.values

    def insert(self, val: int) -> bool:
        if val in self.index_of:
            return False
        self.index_of[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.index_of:
            return False
        # move the last value into val's slot, then pop the end — O(1)
        i = self.index_of[val]
        last = self.values[-1]
        self.values[i] = last
        self.index_of[last] = i
        self.values.pop()
        del self.index_of[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.values)
