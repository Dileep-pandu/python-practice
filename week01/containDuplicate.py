class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        # Time: O(n), Space: O(n)
        seen = set()
        for x in nums:
            if x in seen:        # O(1) lookup
                return True
            seen.add(x)
        return False


    # class Solution:
    # def containsDuplicate(self, nums: list[int]) -> bool:
    #     # Time: O(n), Space: O(n)
    #     return len(set(nums)) != len(nums)