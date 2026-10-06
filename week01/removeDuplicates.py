class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        # Time: O(n), Space: O(1)
        write = 1                          # nums[0] is always unique
        for read in range(1, len(nums)):
            if nums[read] != nums[read - 1]:
                nums[write] = nums[read]
                write += 1
        return write