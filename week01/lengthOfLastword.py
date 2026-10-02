class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        # Time: O(n), Space: O(n) — split creates a list
        return len(s.split()[-1])