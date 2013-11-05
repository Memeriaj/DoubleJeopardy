import sys


class CSVParser(object):
    trainingData = "../tgmctrain.csv"
    #trainingData = "../refinedTraining.csv"
    evalData = "../tgmcevaluation.csv"
    #evalData = "../reducedEvaluation.csv"
    csvData = []

    @staticmethod
    def parseTrainingData():
        CSVParser.parseAndStoreLineData(CSVParser.trainingData)

    @staticmethod
    def parseEvalData():
        CSVParser.parseAndStoreEvalData(CSVParser.evalData)

    @staticmethod
    def getData():
        return CSVParser.csvData

    @staticmethod
    def getSeparatedData():
        falses = []
        trues = []
        for answer in CSVParser.csvData:
            if answer[2] == 1:
                trues.append(answer)
            else:
                falses.append(answer)
        return falses, trues

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
                trueFalse = 1
                stringBool = separatedLine[-1].rstrip("\n")
                if stringBool == 'false' or stringBool == 'false\n' or stringBool == 'False\n' or stringBool == 'False':
                    trueFalse = 0
                elif stringBool == 'true' or stringBool == 'true\n' or stringBool == 'True\n' or stringBool == 'True':
                    trueFalse = 1
                else:
                    print "WE DIDN'T FIND A BOOLEAN!!!!"
                    return
                    #print "String Bool: ", stringBool
                #print "Converted: ",trueFalse
                CSVParser.csvData.append((questionKey, answerKey, trueFalse, answerValues))

    @staticmethod
    def parseAndStoreEvalData(fileToParse):
        with open(fileToParse) as inFile:
            CSVParser.csvData = []
            for line in inFile:
                separatedLine = line.split(',')
                answerValues = []
                for index in range(2, len(separatedLine) - 1):
                    answerValues.append(float(separatedLine[index]))
                questionKey = int(float(separatedLine[1]))
                answerKey = int(float(separatedLine[0]))

                CSVParser.csvData.append((questionKey, answerKey, answerValues))
