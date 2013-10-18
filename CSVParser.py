import sys
import pyavltree
from pyavltree import AVLTree


class CSVParser(object):
    trainingData = "tgmctrain.csv"
    evalData = "tgmcevaluation.csv"
    csvData = []

    @staticmethod
    def parseTrainingData():
        CSVParser.parseAndStoreLineData(CSVParser.trainingData)

    @staticmethod
    def parseEvalData():
        CSVParser.parseAndStoreLineData(CSVParser.evalData)

    @staticmethod
    def getData():
        return CSVParser.csvData

    @staticmethod
    def parseAndStoreLineData(fileToParse):
        with open(fileToParse) as inFile:
            CSVParser.csvData = []
            for line in inFile:
                separatedLine = line.split(',')
                answerValues = []
                for index in range(2, len(separatedLine) - 2):
                    answerValues.append(float(separatedLine[index]))
                questionKey = int(float(separatedLine[1]))
                answerKey = int(float(separatedLine[0]))
                trueFalse = False
                stringBool = separatedLine[-1].rstrip("\n")
                if stringBool == 'false':
                    trueFalse = False
                elif stringBool == 'true':
                    trueFalse = True
                else:
                    print "WE DIDN'T FIND A BOOLEAN!!!!"
                    return
                    #print "String Bool: ", stringBool
                #print "Converted: ",trueFalse
                CSVParser.csvData.append((questionKey, answerKey, trueFalse, answerValues))
