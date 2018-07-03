import csv
import os

from DataSetNormalization.DefsNormalization import replaceInvalidArguments, removeExpendableAttribute, moveLastPositionInterestClass
from DataSetNormalization.DefsNormalization import replaceAccentuationAndUpperCase, normalizeNORMALXANORMAL
from DataSetNormalization.DefsNormalization import normalizeSEXO, normalizePESO, normalizeIDADE, normalizeIMC

# Directory containing the original dataset in csv UTF-8
dataSetCSVDirectory = '../DataSet/'

# Original dataset in csv UTF-8
dataSetCSVInput = dataSetCSVDirectory + 'DataSet.csv'

# Normalized dataset output
dataSetCSVOutput = dataSetCSVDirectory + 'DataSetNormalization.csv'

# Removes output dataset before execution
if os.path.isfile(dataSetCSVOutput):
    os.remove(dataSetCSVOutput)

# Read Original DataSet exections functions normalization write DataSet Ouput
with open(dataSetCSVOutput, 'w', newline='', encoding='utf-8') as csvWriterFile:
    writerCSV = csv.writer(csvWriterFile)

    with open(dataSetCSVInput, newline='', encoding='utf-8') as csvReaderFile:
        readerCSV = csv.reader(csvReaderFile)

        for row in readerCSV:
            line = replaceInvalidArguments(row)
            line = replaceAccentuationAndUpperCase(line)

            line = normalizeNORMALXANORMAL(line)
            line = normalizeSEXO(line)
            line = normalizePESO(line)
            line = normalizeIDADE(line)
            line = normalizeIMC(line)

            line = moveLastPositionInterestClass(line)
            line = removeExpendableAttribute(line)
            writerCSV.writerow(line)