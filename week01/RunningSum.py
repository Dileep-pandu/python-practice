class Solution:
    def runningSum(self, nums: list[int]) -> list[int]:
        # Time: O(n), Space: O(n) for the result
        result = []
        total = 0
        for x in nums:
            total += x
            result.append(total)
        return result