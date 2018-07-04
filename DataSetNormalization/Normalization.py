import csv
import os
from DataSetNormalization.DefsNormalization import DefsNormalization

# Moldable Parameters for Data Normalization
maxValueFC = 250
minValueFC = 10
maxValueIMC = 60.0
minValueIMC = 1.0
maxValueAge = 120
minValueAge = 0
maxValueWeight = 500.0
minValueWeight = 0.1
maxValueHeight = 350
minValueHeight = 1
removePAS = True  # Remove height and weight attributes pa's systolic and diastolic
removeAlturaAndPeso = True  # Remove height and weight attributes from dataset
missingValuesGenere = True  # Replaces the UNDEFINED genders with missing values
maxValueToConversionHeight = 4

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
            normalization = DefsNormalization(maxValueFC, minValueFC, maxValueIMC, minValueIMC, maxValueAge,
                                              minValueAge, maxValueWeight, minValueWeight, maxValueHeight,
                                              minValueHeight, removePAS, removeAlturaAndPeso, missingValuesGenere,
                                              maxValueToConversionHeight)

            line = normalization.replaceInvalidInterestArguments(row)
            line = normalization.replaceAccentuationAndUpperCase(line)

            line = normalization.normalizeNORMALXANORMAL(line)
            line = normalization.normalizeSEXO(line)
            line = normalization.normalizeIDADE(line)
            line = normalization.normalizeIMC(line)
            line = normalization.normalizeFC(line)

            line = normalization.moveLastPositionInterestClass(line)
            line = normalization.removeExpendableAttribute(line)
            writerCSV.writerow(line)
