class NoMoveSimulation:

    
    def __init__(self, resolution: int) -> None:
        self.resolution = resolution
        self.iteration  = 0

    def updatePreyPosition(self):
        pass

    def run(self):
        self.iteration += 1

    def simulationOver(self):
        pass

    def getReferenceVectors(self):
        pass

    def getError(self):
        pass