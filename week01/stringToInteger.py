class Solution:
    def myAtoi(self, s: str) -> int:
        # Time: O(n), Space: O(1)
        INT_MAX, INT_MIN = 2**31 - 1, -2**31
        i, n = 0, len(s)

        # 1. Skip leading spaces
        while i < n and s[i] == " ":
            i += 1

        # 2. Optional sign
        sign = 1
        if i < n and s[i] in "+-":
            if s[i] == "-":
                sign = -1
            i += 1

        # 3. Read digits
        result = 0
        while i < n and s[i].isdigit():
            result = result * 10 + int(s[i])
            i += 1

        # 4 & 5. Apply sign and clamp
        result *= sign
        if result > INT_MAX:
            return INT_MAX
        if result < INT_MIN:
            return INT_MIN
        return result