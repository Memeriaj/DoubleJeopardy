__author__ = 'Icarus'
from CSVParser import *
from backpropNetwork import *
from networkTrainer import *
import random

def main():
    CSVParser.parseTrainingData()
    data = CSVParser.getData()
    falseData, trueData = CSVParser.getSeparatedData()
    print "False data size: ", len(falseData)
    print "True Data size: ", len(trueData)
    sampledFalses = randomSampleOfData(falseData, len(trueData))
    sampledData = layer_answers(trueData, sampledFalses)
    print "Training Size: ", len(sampledData)
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

def layer_answers(true_data, false_data):
    if len(true_data) != len(false_data):
        print "For some reason, there are different numbers of trues and falses"
        return []
    to_return = []
    for i in range(0, len(false_data)):
        to_return.append(false_data[i])
        to_return.append(true_data[i])
    return to_return


if __name__ == '__main__':
    main()
