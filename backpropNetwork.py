__author__ = 'Icarus'
from networkLayer import *

class BackpropNetwork:
    def __init__(self, numberOfNodesList, learningRate, momentum):
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
            self.layers[i].feedForward()

            if i != self.numberOfLayers-1:
                self.layers[i+1].inputs = self.layers[i].getOutputs()

    def updateWeights(self, expectedOutput):
        self.calculateSignalErrors(expectedOutput)
        self.backpropagateError()

    def calculateSignalErrors(self, expectedOutputBool):
        outputLayerIndex = self.numberOfLayers-1
        expectedOutput = 0
        if expectedOutputBool:
            expectedOutput = 1
        for i in range(0, len(self.layers[outputLayerIndex].neurons)):
            self.layers[outputLayerIndex].neurons[i].signalError = (expectedOutput - self.layers[outputLayerIndex].neurons[i].output) * \
                                                                    self.layers[outputLayerIndex].neurons[i].output * \
                                                                    (1 - self.layers[outputLayerIndex].neurons[i].output)
        for i in range(self.numberOfLayers-2, 0, -1):
            for j in range(0, len(self.layers[i].neurons)):
                errorSum = 0
                for k in range(0, len(self.layers[i+1].neurons)):
                    errorSum = errorSum + self.layers[i+1].neurons[k].weights[j] * self.layers[i+1].neurons[k].signalError

                self.layers[i].neurons[j].signalError = self.layers[i].neurons[j].output * (1 - self.layers[i].neurons[j].output) * errorSum

    def backpropagateError(self):
        for i in range(self.numberOfLayers-1, 0, -1):
            for j in range(0, len(self.layers[i].neurons)):
                threshDiff = self.learningRate * self.layers[i].neurons[j].signalError + self.momentum * self.layers[i].neurons[j].thresholdDiff
                self.layers[i].neurons[j].thresholdDiff = threshDiff
                self.layers[i].neurons[j].threshold = self.layers[i].neurons[j].threshold + threshDiff
                for k in range(0, len(self.layers[i].inputs)):
                    weightDiff = self.learningRate*self.layers[i].neurons[j].signalError*self.layers[i-1].neurons[k].output + \
                                 self.momentum*self.layers[i].neurons[j].weightDiffs[k]
                    self.layers[i].neurons[j].weightDiffs[k] = weightDiff
                    self.layers[i].neurons[j].weights[k] = self.layers[i].neurons[j].weights[k] + weightDiff

    def calculateOverallError(self, numberOfTests, actualOutputs, expectedOutputs):
        errorSum = 0
        for i in range(0, numberOfTests):
            for j in range(0, len(self.layers[self.numberOfLayers-1].neurons)):
                expectedOutput = 0
                if expectedOutputs[i]:
                    expectedOutput = 1
                errorSum = errorSum + 0.5*((expectedOutput- actualOutputs[i])**2)
        return errorSum

    def getNetworkOutput(self):
        return self.layers[self.numberOfLayers-1].neurons[0].getOutput()

    def toFile(self):
#        TODO: Add code to make the network be saved to a file, for later loading/refinement
        return

    def fromFile(self, fileContents):
#        TODO: Add code for creating a network from the contents of a file
        return
