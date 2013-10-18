__author__ = 'Icarus'
from CSVParser import *

def main():
    CSVParser.parseTrainingData()
    data = CSVParser.getData()


if __name__ == '__main__':
    main()
