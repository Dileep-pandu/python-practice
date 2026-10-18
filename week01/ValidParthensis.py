class Solution:
    def isValid(self, s: str) -> bool:
        # Time: O(n), Space: O(n)
        pairs = {")": "(", "]": "[", "}": "{"}   # closer → opener
        stack = []
        for ch in s:
            if ch in pairs:                       # closing bracket
                if not stack or stack[-1] != pairs[ch]:
                    return False
                stack.pop()
            else:                                 # opening bracket
                stack.append(ch)
        return not stack                          # empty → True