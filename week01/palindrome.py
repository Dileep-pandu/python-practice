class Solution:
    def isPalindrome(self, s: str) -> bool:
        # Time: O(n), Space: O(n)
        cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
        return cleaned == cleaned[::-1]
if __name__ == "__main__":
    sol = Solution()
    assert sol.isPalindrome("A man, a plan, a canal: Panama") is True
    assert sol.isPalindrome("race a car") is False
    assert sol.isPalindrome(" ") is True       # edge case: empty after cleaning
    print("All tests passed")