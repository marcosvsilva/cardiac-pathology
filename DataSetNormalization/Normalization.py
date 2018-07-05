import csv
import os
from DataSetNormalization.DefsNormalization import DefsNormalization, getAttributesDataSet

# Moldable Parameters for Data Normalization

maxValueFC = 200
minValueFC = 40

maxValuePA = 200
minValuePA = 50

maxValueIMC = 60.0
minValueIMC = 1.0

maxValueAge = 120
minValueAge = 0

maxValueWeight = 500.0
minValueWeight = 0.1

maxValueHeight = 350
minValueHeight = 1

attributesRemove = []  # Remove attributes unnecessary from dataset
missingValuesGenere = True  # Replaces the UNDEFINED genders with missing values
maxValueToConversionHeight = 4  # Maximum value to express height in meters, so that no conversion is required

# Remove attributes unnecessary from dataset
attributesDataSet = getAttributesDataSet()

attributesRemove.append(attributesDataSet['HDA2'])
attributesRemove.append(attributesDataSet['PADIASTOLICA'])
attributesRemove.append(attributesDataSet['PASISTOLICA'])
attributesRemove.append(attributesDataSet['CONVERNIO'])
attributesRemove.append(attributesDataSet['ANIVERSARIO'])
attributesRemove.append(attributesDataSet['ATENDIMENTO'])
attributesRemove.append(attributesDataSet['ALTURA'])
attributesRemove.append(attributesDataSet['PESO'])
attributesRemove.append(attributesDataSet['ID'])

indexInterestClass = 4

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
            normalization = DefsNormalization(maxValueFC, minValueFC, maxValuePA, minValuePA, maxValueIMC, minValueIMC,
                                              maxValueAge, minValueAge, maxValueWeight, minValueWeight, maxValueHeight,
                                              minValueHeight, attributesRemove, missingValuesGenere,
                                              maxValueToConversionHeight)

            line = normalization.replaceInvalidInterestArguments(row)
            line = normalization.replaceAccentuationAndUpperCase(line)

            line = normalization.normalizeNORMALXANORMAL(line)
            line = normalization.normalizeSEXO(line)
            line = normalization.normalizeIDADE(line)
            line = normalization.normalizeIMC(line)
            line = normalization.normalizeFC(line)
            line = normalization.normalizePPA(line)

            line = normalization.removeExpendableAttribute(line)
            line = normalization.moveLastPositionInterestClass(line, indexInterestClass)
            writerCSV.writerow(line)
