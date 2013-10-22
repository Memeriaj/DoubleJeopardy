__author__ = 'Icarus'
from CSVParser import *
from backpropNetwork import *
from networkTrainer import *
import random

def main():
    CSVParser.parseTrainingData()
    data = CSVParser.getData()
    falseData, trueData = CSVParser.getSeparatedData()
    sampledFalses = randomSampleOfData(falseData, len(trueData))
    sampledData = []
    sampledData.extend(trueData)
    sampledData.extend(sampledFalses)
    print "Finished Getting Data"
    momentum = 0.3
    learningRate = 0.01
    #networkSizeList = [len(data[0][3]), 6, 4, 2, 1]
    networkSizeList = [len(data[0][3]), 40, 1]
    #networkSizeList = [len(data[0][3]), 600, 400, 200, 100, 50, 40, 20, 8, 1]
    #networkSizeList = [len(data[0][3]), 10, 10, 10, 10, 5, 4, 4, 2, 1]
    #networkSizeList = [len(data[0][3]), 60, 40, 20, 1]
    network = BackpropNetwork(networkSizeList, learningRate, momentum)

    NetworkTrainer.trainNetwork(network, sampledData, 10, 1)
    print "Done learning, that's neat"
    #TODO: Write code to save the network after it is done running
    #f = open("NeuralNetworkConfigurations/trained.nn", "w")
    #f.write(network.toFile())


def randomSampleOfData(falseData, numberToSample):
    randomData = []
    uniqueIndexes = 0
    indexes = []
    while uniqueIndexes < numberToSample:
        index = random.randrange(0, len(falseData))
        if index not in indexes:
            indexes.append(index)
            randomData.append(falseData[index])
            uniqueIndexes += 1
    return randomData


if __name__ == '__main__':
    main()
