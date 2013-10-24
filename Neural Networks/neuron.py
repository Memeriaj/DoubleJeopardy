__author__ = 'Icarus'

import random

class Neuron:

    def __init__(self, numOfInputs):
        self.numberOfInputs = numOfInputs
        self.weights = []
        self.weightDiffs = []
        self.threshold = random.uniform(-1, 1)
        self.thresholdDiff = 0
        self.output = None
        self.signalError = None
        for i in range(0, numOfInputs):
            self.weights.append(random.uniform(-1, 1))
            self.weightDiffs.append(0)

    def getWeights(self):
        return self.weights

    def getOutput(self):
        return self.output

