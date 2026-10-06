class Solution:
    def fib(self, n: int) -> int:
        # Time: O(n), Space: O(1)
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b      # tuple swap from Day 2
        return a