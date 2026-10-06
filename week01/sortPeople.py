class Solution:
    def sortPeople(self, names: list[str], heights: list[int]) -> list[str]:
        # Time: O(n log n), Space: O(n)
        people = list(zip(names, heights))
        # [('Mary', 180), ('John', 165), ('Emma', 170)]
        people.sort(key=lambda p: p[1], reverse=True)
        return [name for name, _ in people]