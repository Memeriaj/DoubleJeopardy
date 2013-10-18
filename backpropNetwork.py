__author__ = 'Icarus'
from networkLayer import *

class BackpropNetwork:
    def __init__(self, numberOfNodesList, learningRate, momentum, minError, maximumIter):
        self.minimumError = minError
        self.maxIterations = maximumIter
        self.learningRate = learningRate
        self.momentum = momentum
        self.layers = []
        self.numberOfLayers = len(numberOfNodesList)

        newLayer = NetworkLayer(numberOfNodesList[0], numberOfNodesList[0])
        self.layers.append(newLayer)

        for i in range(1, self.numberOfLayers):
            newLayer = NetworkLayer(numberOfNodesList[i], numberOfNodesList[i-1])
            self.layers.append(newLayer)

    def feedForward(self, inputData):
        self.layers[0].inputs = inputData
        for i in range(0, len(self.layers[0].neurons)):
            self.layers[0].neurons[i].output = self.layers[0].inputs[i]

        self.layers[1].inputs = self.layers[0].inputs

        for i in range(1, self.numberOfLayers):
            self.layer[i].feedForward()

            if i != self.numberOfLayers-1:
                self.layers[i+1].inputs = self.layers[i].getOutputs()

    def updateWeights(self):
        self.calculateSignalErrors()
        self.backpropagateError()

    def calculateSignalErrors(self, expectedOutput):
        outputLayerIndex = self.numberOfLayers-1

        for i in range(0, len(self.layers[outputLayerIndex].neurons)):
            self.layers[outputLayerIndex].neurons[i].signalError = (expectedOutput - self.layers[outputLayerIndex].neurons[i].output) * \
                                                                    self.layers[outputLayerIndex].neurons[i].output * \
                                                                    (1 - self.layers[outputLayerIndex].neurons[i].output)
        for i in range(self.numberOfLayers-2, 0):
            for j in range(0, len(self.layers[i].neurons)):
                errorSum = 0
                for k in range(0, len(self.layers[i+1].neurons)):
                    errorSum = errorSum + self.layers[i+1].neurons[k].weights[j] * self.layers[i+1].neurons[k].signalError

                self.layers[i].neurons[j].signalError = self.layers[i].neurons[j].output * (1 - self.layers[i].neurons[j].output) * errorSum
                