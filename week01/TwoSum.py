class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        # Time: O(n), Space: O(n)
        seen = {}                       # value -> index
        for i, num in enumerate(nums):
            needed = target - num
            if needed in seen:
                return [seen[needed], i]
            seen[num] = i