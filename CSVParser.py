import sys
import pyavltree
from pyavltree import AVLTree

fileToParse = "tgmctrain.csv"
# action = lambda dataLine: print
csvData = AVLTree()

def parseAndStoreLineData(fileToParse):
    with open(fileToParse) as inFile:
        for line in inFile:
            separatedLine = line.split(',')
            answerValues = []
            for index in range(2, len(separatedLine)-1):
                answerValues.append(float(separatedLine[index]))
            questionKey = int(float(separatedLine[1]))
            answerKey = int(float(separatedLine[0]))
            if questionKey not in csvData:
            #    The question is not in the dictionary, so we should add the question to the dictionary, and then the answer to the question's dictionary
                csvData[questionKey] = []
            print "Answer: ", answerKey
            print "Questions: ", len(csvData.keys())
            csvData[questionKey].append((answerKey, (answerValues, separatedLine[len(separatedLine)-1])))
        numberOfQuestions = len(csvData.keys())
        print "Number of Questions: ", numberOfQuestions
        print "Question Numbers: "
        for key in csvData:
            print key


parseAndStoreLineData(fileToParse)
