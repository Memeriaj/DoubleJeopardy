__author__ = 'Icarus'
from backpropNetwork import *

class NetworkTrainer:

    @staticmethod
    def trainNetwork(network, inputData, maxIterations, minError):
        iteration = 0
        expectedOutputs = []
        actualOutputs = []
        overallError = None
        errorCount = 0
        lastError = None
        #Since there is no do-while in python, we'll just do this...
        firstTime = True
        while firstTime or (iteration < maxIterations and ((overallError is None) or overallError > minError)):
            print "On learning Iteration #", iteration, " Out of ", maxIterations
            #since the data is in the form (QID, AID, Answer, Data) just get the data
            answerNumber = 0
            for answer in inputData:
                network.feedForward(answer[3])
                actualOutputs.append(network.getNetworkOutput())
                expectedOutputs.append(answer[2])
                network.updateWeights(answer[2])

                if answerNumber%1000 == 0:
                    print "On answer ", answerNumber

                answerNumber += 1
            print "Actual Outputs: ", actualOutputs
            overallError = network.calculateOverallError(len(inputData), actualOutputs, expectedOutputs)

            print "Overall Error: ", overallError
            print ""

            if lastError is None:
                lastError = overallError
            elif abs(overallError - lastError) < 1:
                errorCount += 1

            if errorCount >= 0:
                print "No notable change, let's check how we're doing"
                numRight = 0
                numTrue = 0
                numTrueAndRight = 0
                for answer in range(0, len(expectedOutputs)):
                    if actualOutputs[answer] > 0.5:
                        actual = True
                    else:
                        actual = False
                    expected = expectedOutputs[answer]
                    if actual == expected:
                        numRight += 1
                        if actual == True:
                            numTrueAndRight += 1
                    if actual == True:
                        numTrue += 1
                print "Out of ", len(actualOutputs), "answers, there were ", numTrue, "found to be true, with ", numRight, "correct, and ", numTrueAndRight, "both True and correct"
            lastError = overallError
            actualOutputs = []
            expectedOutputs = []
            iteration += 1
            firstTime = False
