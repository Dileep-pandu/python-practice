class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        # Time: O(S) where S = total characters, Space: O(1)
        prefix = strs[0]
        for word in strs[1:]:
            while not word.startswith(prefix):
                prefix = prefix[:-1]          # drop last character
                if not prefix:
                    return ""
        return prefix