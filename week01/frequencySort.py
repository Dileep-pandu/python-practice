from collections import Counter

class Solution:
    def frequencySort(self, nums: list[int]) -> list[int]:
        # Time: O(n log n), Space: O(n)
        freq = Counter(nums)
        return sorted(nums, key=lambda x: (freq[x], -x))