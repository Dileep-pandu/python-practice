class MyHashMap:
    # Time: O(n / size) per call on average, Space: O(size + n)

    def __init__(self):
        self.size = 1000
        # each bucket holds [key, value] pairs
        self.buckets = [[] for _ in range(self.size)]

    def _bucket(self, key: int) -> list:
        return self.buckets[key % self.size]

    def put(self, key: int, value: int) -> None:
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value     # key exists — update in place
                return
        bucket.append([key, value])

    def get(self, key: int) -> int:
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return
