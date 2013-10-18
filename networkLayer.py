__author__ = 'Icarus'

from neuron import Neuron
import math

class NetworkLayer:
    def __init__(self, numberOfNeurons, numberOfInputs):
        self.neurons = []
        self.inputs = []
        for i in range(0, numberOfNeurons):
            self.neurons.append(Neuron(numberOfInputs))

    def getOutputs(self):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.getOutput())
        return outputs

    @staticmethod
    def sigmoid(self, netValue):
        return 1.0/(1 + math.exp(-netValue))

    def feedForward(self):
        for i in range(0, len(self.neurons)):
            netValue = self.neurons[i].threshold

            for j in range(0, len(self.neurons[i].weights)):
                netValue = netValue + self.inputs[j] * self.neurons[i].weights[j]

            self.neurons[i].output = NetworkLayer.sigmoid(netValue)