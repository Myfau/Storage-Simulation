import numpy as np


class Gene:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, shelf):
        xDis = abs(self.x - shelf.x)
        yDis = abs(self.y - shelf.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance
