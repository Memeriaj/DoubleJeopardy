__author__ = 'Icarus'
from CSVParser import *
import random
from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import *
from pybrain.supervised.trainers import BackpropTrainer
import pickle

def main():
    get_eval_results()

def train_and_save_network():
    CSVParser.parseTrainingData()

    data = CSVParser.getData()

    false_data, true_data = CSVParser.getSeparatedData()

    sampled_data = []
    sampled_falses = random_sample_of_data(false_data, len(true_data))

    sampled_data = layer_answers(true_data, sampled_falses)

    print "Finished Getting Data"

    #network_size_list = [len(data[0][3]), 6, 4, 2, 1]
    network_size_list = [len(data[0][3]), 40, 1]
    #network_size_list = [len(data[0][3]), 600, 400, 200, 100, 50, 40, 20, 8, 1]
    #network_size_list = [len(data[0][3]), 10, 10, 10, 10, 5, 4, 4, 2, 1]
    #network_size_list = [len(data[0][3]), 60, 40, 20, 1]

    pybrain_dataset = SupervisedDataSet(len(data[0][3]), 1)
    add_samples_to_pybrain_dataset(pybrain_dataset, sampled_data)

    network = buildNetwork(len(data[0][3]), 100, 1, bias=True,
                           hiddenclass=SigmoidLayer, outclass=SigmoidLayer)

    print "Made the network, now making the trainer"
    trainer = BackpropTrainer(network, pybrain_dataset, 0.01, 1.0, 0.3)
    print "Made the trainer, now training for 10 epochs"
    error = trainer.trainUntilConvergence(None, 50, True, 50)

    print "Now time to check performance"
    check_network_against_dataset(network, sampled_data)

    #TODO: Write code to save the network after it is done running
    f = open("../NeuralNetworkConfigurations/trainedMedium.nn", "w")
    pickle.dump(network, f)
    f.close()


def get_eval_results():
    CSVParser.parseEvalData()

    data = CSVParser.getData()

    print "Finished Getting Data"

    f = open("../NeuralNetworkConfigurations/trained.nn", "r")
    network = pickle.load(f)
    answers = []

    for answer_candidate in data:
        output = network.activate(answer_candidate[2])
        if output > 0.5:
            answers.append(answer_candidate[1])

    #TODO: Write code to save the network after it is done running
    f = open("../answersToCheck.txt", "w")
    for to_print in answers:
        string = str(to_print)+"\n"
        hello = string
        count = hello.count("0")
        f.write(string)
    f.close()


def random_sample_of_data(falseData, numberToSample):
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

def add_samples_to_pybrain_dataset(pybrain_set, data_to_add):
    for answer in data_to_add:
        pybrain_set.addSample(answer[3], (answer[2]))

def check_network_against_dataset(network, sampled_data):
    number_correct = 0
    number_true = 0
    number_true_and_correct = 0
    for answer in sampled_data:
        evidence_data = answer[3]
        expected_answer_val = answer[2]
        network_answer_val = network.activate(evidence_data)
        expected_bool = False
        if expected_answer_val > 0.5:
            expected_bool = True
        network_bool = False
        if network_answer_val > 0.5:
            network_bool = True

        if network_bool:
            number_true += 1
        if network_bool == expected_bool:
            number_correct += 1
            if network_bool:
                number_true_and_correct += 1
    print "After checking all the training data, these are the results:"
    print "Number correct: ", number_correct
    print "Number found True: ", number_true
    print "Number found accurately found True: ", number_true_and_correct

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
