import sys

fileToParse = "testCSV.txt"
# action = lambda dataLine: print

def parseAndDoSomethingToLineData(fileToParse):
    with open(fileToParse) as inFile:
        for line in inFile:
            seperatedLine = line.split(',')
            print seperatedLine


parseAndDoSomethingToLineData(fileToParse)
