__author__ = 'Icarus'
from CSVParser import *
import random
import pickle
from decisions import *


def main():
    get_eval_results()


def train_and_save_network():
    CSVParser.parseTrainingData()

    data = CSVParser.getData()

    false_data, true_data = CSVParser.getSeparatedData()
    all_data = list()
    all_data.extend(false_data)
    all_data.extend(true_data)
    all_tree_data, all_tree_answers = return_data_and_answers_separately(all_data)

    trees = list()
    max_index = 0
    max_score = 0
    for k in range(0, 2):
        #sampled_falses = random_sample_of_data(false_data, len(true_data))
        #sampled_data = layer_answers(true_data, sampled_falses)
        #sampled_tree_data, sampled_tree_answers = return_data_and_answers_separately(sampled_data)
        sampled_tree_data = all_tree_data
        sampled_tree_answers = all_tree_answers
        #tree = ID3(sampled_tree_data, sampled_tree_answers, range(0, len(sampled_tree_data[0])))
        tree = ID3(all_tree_data, all_tree_answers, range(0, len(all_tree_data[0])))
        trees.append(tree)
        tree_results = list()
        for line in sampled_tree_data:
            tree_results.append(getAnswer(line, tree))

        number_correct = 0
        number_true = 0
        number_true_and_correct = 0
        for i in range(0, len(sampled_tree_answers)):
            expected = sampled_tree_answers[i]
            if expected == 0:
                expected = False
            else:
                expected = True
            actual = tree_results[i]
            if actual:
                number_true += 1
            if expected == actual:
                number_correct += 1
                if actual:
                    number_true_and_correct += 1
        print "Out of ", len(sampled_tree_answers), "answers, ", number_correct, " were answered correctly, with ", number_true, " found true, and ", number_true_and_correct, " of those ACTUALLY being true"
        score = number_true_and_correct - (number_true - number_true_and_correct)
        if score > max_score:
            max_score = score
            max_index = k
    print "Max Score: ", max_score
    f = open("../DecisionTreesRedux/optimalSampledTree.dt", "w")
    pickle.dump(trees[max_index], f)
    f.close()


def get_eval_results():
    CSVParser.parseEvalData()

    data = CSVParser.getData()

    print "Finished Getting Data"

    f = open("../DecisionTreesRedux/optimalSampledTree.dt", "r")
    tree = pickle.load(f)
    answers = []

    for answer_candidate in data:
        output = getAnswer(answer_candidate[2], tree)
        if output is True:
            answers.append(answer_candidate[1])
    print "Answers found True: ", len(answers)
    f = open("../answersToCheck.txt", "w")
    for to_print in answers:
        string = str(to_print) + "\n"
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


def return_data_and_answers_separately(data):
    data_list = list()
    answers = list()
    for row_info in data:
        qid = row_info[0]
        aid = row_info[1]
        bool_answer = row_info[2]
        row_data = row_info[3]
        data_list.append(row_data)
        answers.append(bool_answer)
    return data_list, answers


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
