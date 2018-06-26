import csv
import os
from unicodedata import normalize

#Directory containing the original dataset in csv UTF-8
DataSetCSVDirectory = '../DataSet/'

#Original dataset in csv UTF-8
DataSetCSVInput = DataSetCSVDirectory + 'DataSet.csv'

#Normalized dataset output
DataSetCSVOutput = DataSetCSVDirectory + 'DataSetNormalization.csv'

#Removes output dataset before execution
if os.path.isfile(DataSetCSVOutput):
    os.remove(DataSetCSVOutput)

def replaceInvalidArguments(line):
    if '#VALUE!' in line:
        index = line.index('#VALUE!')
        line[index] = ''
        replaceInvalidArguments(line)
    return line

def replaceAccentuation(line):
    for i in range(len(line)):
        line[i] = normalize('NFKD', line[i]).encode('ASCII', 'ignore').decode('ASCII')
    return line

#Read Original DataSet exections functions normalization write DataSet Ouput
with open(DataSetCSVOutput, 'w', newline='', encoding='utf-8') as csvWriterFile:
    writerCSV = csv.writer(csvWriterFile)

    with open(DataSetCSVInput, newline='', encoding='utf-8') as csvReaderFile:
        readerCSV = csv.reader(csvReaderFile)
        for row in readerCSV:
            line = replaceInvalidArguments(row)
            line = replaceAccentuation(line)
            writerCSV.writerow(line)