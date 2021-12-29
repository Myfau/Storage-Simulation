class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    def routeDistance(self):
        if self.distance == 0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromBox = self.route[i]
                toBox = None
                if i + 1 < len(self.route):
                    toBox = self.route[i + 1]
                else:
                    toBox = self.route[0]
                pathDistance += fromBox.distance(toBox)
            self.distance = pathDistance
        return self.distance

    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness
