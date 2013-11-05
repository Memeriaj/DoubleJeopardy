__author__ = 'Icarus'
from CSVParser import *
import random
import pickle
from sklearn.linear_model.logistic import *


def main():
    CSVParser.parseTrainingData()
    data = CSVParser.getData()

    false_data, true_data = CSVParser.getSeparatedData()
    best_reg = train_and_save_network(false_data, true_data)
    train_second_layer_reg(false_data, true_data)
    #reduced, ids = get_eval_results()
    #get_eval_second_tier_results(reduced, ids)


def train_and_save_network(false_data, true_data):

    ##all_data = list()
    ##all_data.extend(false_data)
    ##all_data.extend(true_data)
    ##all_reg_data, all_reg_answers = return_data_and_answers_separately(all_data)
    #
    #sampled_reg_data = all_reg_data
    #sampled_reg_answers = all_reg_answers
    max_score = 0
    max_index = 0
    regs = list()
    for k in range(0, 20):
        sampled_falses = random_sample_of_data(false_data, len(true_data))
        sampled_data = layer_answers(true_data, sampled_falses)
        sampled_reg_data, sampled_reg_answers = return_data_and_answers_separately(sampled_data)

        train_set, test_set = sampled_reg_data[:-500], sampled_reg_data[-500:]
        train_answers, test_answers = sampled_reg_answers[:-500], sampled_reg_answers[-500:]
        reg = LogisticRegression(penalty='l2', dual=False, tol=1e-10, C=1.0, fit_intercept=True, intercept_scaling=1,
                                 class_weight=None)
        regs.append(reg)
        reg.fit(train_set, train_answers)
        reg_results = reg.predict(test_set)
        number_correct = 0
        number_true = 0
        number_true_and_correct = 0
        for i in range(0, len(test_answers)):
            expected = test_answers[i]
            actual = reg_results[i]
            actual_bool = False
            expected_bool = False
            if actual > 0:
                number_true += 1
                actual_bool = True
            if expected > 0:
                expected_bool = True

            if actual_bool == expected_bool:
                number_correct += 1
                if actual_bool:
                    number_true_and_correct += 1
        score = number_true_and_correct - (number_true - number_true_and_correct)
        if score > max_score:
            max_score = score
            max_index = k
        print "Out of ", len(test_answers), " candidates, ", number_correct, " were correctly identified, with ", \
            number_true, " found to be True, and ", number_true_and_correct, \
            " BOTH TRUE AND CORRECT, this is a ration of: ", (1.0*number_true_and_correct)/(1.0 * number_true), \
            "which would get a score of: ", number_true_and_correct - (number_true - number_true_and_correct)

    f = open("../LogisticRegression/l2Reg.reg", "w")
    pickle.dump(regs[max_index], f)
    f.close()
    return regs[max_index]


def train_second_layer_reg(false_data, true_data, best_reg=None):
    all_data = list()
    all_data.extend(false_data)
    all_data.extend(true_data)
    all_reg_data, all_reg_answers = return_data_and_answers_separately(all_data)

    #sampled_reg_data = all_reg_data
    #sampled_reg_answers = all_reg_answers
    reg = best_reg
    if best_reg is None:
        f = open("../LogisticRegression/l2Reg.reg", "r")
        reg = pickle.load(f)
        f.close()
    reg_reduced_data = list()
    reg_reduced_answers = list()
    for i in range(0, len(all_reg_data)):
        output = reg.predict((all_reg_data[i]))
        if output > 0:
            reg_reduced_data.append(all_reg_data[i])
            reg_reduced_answers.append(all_reg_answers[i])

    train_set, test_set = reg_reduced_data[:(len(reg_reduced_data)/2)], reg_reduced_data[(len(reg_reduced_data)/2):]
    train_answers, test_answers = reg_reduced_answers[:(len(reg_reduced_data)/2)], reg_reduced_answers[(len(reg_reduced_answers)/2):]
    print "train set: ", len(train_set), " train answers : ", len(train_answers)
    print "test set: ", len(test_answers), " test answers : ", len(test_answers)
    print "total: ", len(reg_reduced_data), len(reg_reduced_answers)
    reg = LogisticRegression(penalty='l1', dual=False, tol=1e-10, C=1.0, fit_intercept=True, intercept_scaling=1,
                             class_weight=None)
    reg.fit(train_set, train_answers)
    reg_results = reg.predict(test_set)
    number_correct = 0
    number_true = 0
    number_true_and_correct = 0
    for i in range(0, len(test_answers)):
        expected = test_answers[i]
        actual = reg_results[i]
        actual_bool = False
        expected_bool = False
        if actual > 0:
            number_true += 1
            actual_bool = True
        if expected > 0:
            expected_bool = True

        if actual_bool == expected_bool:
            number_correct += 1
            if actual_bool:
                number_true_and_correct += 1
    score = number_true_and_correct - (number_true - number_true_and_correct)
    print "Out of ", len(test_answers), " candidates, ", number_correct, " were correctly identified, with ", \
        number_true, " found to be True, and ", number_true_and_correct, \
        " BOTH TRUE AND CORRECT, this is a ration of: ", (1.0*number_true_and_correct)/(1.0 * number_true), \
        "which would get a score of: ", number_true_and_correct - (number_true - number_true_and_correct)
    f = open("../LogisticRegression/l1SecondLayerReg.reg", "w")
    pickle.dump(reg, f)
    f.close()


def get_eval_results(print_to_file=False):
    CSVParser.parseEvalData()

    data = CSVParser.getData()

    print "Finished Getting Data"

    f = open("../LogisticRegression/l2Reg.reg", "r")
    reg = pickle.load(f)
    answers = []
    reduced_answers = list()
    for answer_candidate in data:
        output = reg.predict((answer_candidate[2]))
        if output > 0:
            answers.append(answer_candidate[1])
            reduced_answers.append(answer_candidate[2])
    print "Answers found True: ", len(answers)
    if print_to_file:
        f = open("../answersToCheck.txt", "w")
        for to_print in answers:
            string = str(to_print) + "\n"
            f.write(string)
        f.close()
    return reduced_answers, answers


def get_eval_second_tier_results(data, ids):

    f = open("../LogisticRegression/l2SecondLayerReg.reg", "r")
    reg = pickle.load(f)
    answers = []
    for i in range(0, len(data)):
        output = reg.predict(data[i])
        if output > 0:
            answers.append(ids[i])
    print "Answers found True: ", len(answers)
    f = open("../answersToCheck.txt", "w")
    for to_print in answers:
        string = str(to_print) + "\n"
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
        if bool_answer is True or bool_answer == 1:
            bool_answer = 1
        else:
            bool_answer = -1
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
