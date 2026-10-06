from collections import Counter

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Time: O(n), Space: O(1) — at most 26 letters
        return Counter(s) == Counter(t)

# return sorted(s) == sorted(t)    # Time: O(n log n)


# class Solution:
#     def isAnagram(self, s: str, t: str) -> bool:
#         # Time: O(n), Space: O(1)
#         if len(s) != len(t):
#             return False
#         counts = {}
#         for ch in s:
#             counts[ch] = counts.get(ch, 0) + 1   # count up for s
#         for ch in t:
#             counts[ch] = counts.get(ch, 0) - 1   # count down for t
#         return all(v == 0 for v in counts.values())