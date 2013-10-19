__author__ = 'Icarus'
from CSVParser import *
from backpropNetwork import *
from networkTrainer import *

def main():
    CSVParser.parseTrainingData()
    data = CSVParser.getData()
    print "Finished Getting Data"
    momentum = 0.3
    learningRate = 0.01
    networkSizeList = [len(data[0][3]), 6, 4, 2, 1]
    network = BackpropNetwork(networkSizeList, learningRate, momentum)

    NetworkTrainer.trainNetwork(network, data, 2, 1)
    print "Done learning, that's neat"


if __name__ == '__main__':
    main()
