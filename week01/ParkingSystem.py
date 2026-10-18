class ParkingSystem:
    # Time: O(1) per call, Space: O(1)

    def __init__(self, big: int, medium: int, small: int):
        # index 0 is unused so carType 1/2/3 maps directly to the index
        self.spaces = [0, big, medium, small]

    def addCar(self, carType: int) -> bool:
        if self.spaces[carType] > 0:
            self.spaces[carType] -= 1
            return True
        return False