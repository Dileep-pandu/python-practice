from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        # Time: O(n · k log k), n = number of words, k = max word length
        # Space: O(n · k)
        groups = defaultdict(list)
        for word in strs:
            key = "".join(sorted(word))     # "tea" → "aet"
            groups[key].append(word)
        return list(groups.values())