__author__ = 'Icarus'
from backpropNetwork import *

class NetworkTrainer:

    @staticmethod
    def trainNetwork(network, inputData, maxIterations, minError):
        iteration = 0
        expectedOutputs = []
        actualOutputs = []
        overallError = None
        #Since there is no do-while in python, we'll just do this...
        firstTime = True
        while firstTime or (iteration < maxIterations and ((overallError is None) or overallError > minError)):
            #since the data is in the form (QID, AID, Answer, Data) just get the data
            for answer in inputData:
                network.feedForward(answer[3])
                actualOutputs.append(network.getNetworkOutput())
                expectedOutputs.append(answer[2])
                network.updateWeights(answer[2])

            overallError = network.calculateOverallError(len(inputData), actualOutputs, expectedOutputs)
