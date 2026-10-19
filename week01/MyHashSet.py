class MyHashSet:
    # Time: O(n / size) per call on average, Space: O(size + n)

    def __init__(self):
        self.size = 1000
        # one list per bucket — created here so buckets aren't shared
        self.buckets = [[] for _ in range(self.size)]

    def _bucket(self, key: int) -> list:
        return self.buckets[key % self.size]

    def add(self, key: int) -> None:
        bucket = self._bucket(key)
        if key not in bucket:
            bucket.append(key)

    def remove(self, key: int) -> None:
        bucket = self._bucket(key)
        if key in bucket:
            bucket.remove(key)

    def contains(self, key: int) -> bool:
        return key in self._bucket(key)
