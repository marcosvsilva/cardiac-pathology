import csv
import os
from DataSetNormalization.DefsNormalization import DefsNormalization, getAttributesDataSet, getIndexAttributeClass

# Moldable Parameters for Data Normalization

# Max and min values for attributes
maxValueFC = 250
minValueFC = 40

maxValuePA = 250
minValuePA = 40

maxValueIMC = 60.0
minValueIMC = 1.0

maxValueAge = 18
minValueAge = 0

maxValueWeight = 500.0
minValueWeight = 0.1

maxValueHeight = 350
minValueHeight = 1

classDiscretizePESO = [[0, 35], [35, 70], [70, 105], [105, 140], [140, 175]]
classDiscretizeALTURA = [[0, 40], [40, 80], [80, 120], [120, 160], [160, 200]]
classDiscretizeIMC = [[0, 12], [12, 24], [24, 36], [36, 48], [48, 60]]
classDiscretizeIDADE = [[0, 4], [4, 8], [8, 12], [12, 16], [16, 20]]
classDiscretizePAS = [[0, 50], [50, 100], [100, 150], [150, 200], [200, 250]]
classDiscretizePAD = [[0, 50], [50, 100], [100, 150], [150, 200], [200, 250]]
classDiscretizeFC = [[0, 50], [50, 100], [100, 150], [150, 200], [200, 250]]

attributesRemove = []  # Remove attributes unnecessary from dataset
missingValuesGenere = True  # Replaces the UNDEFINED genders with missing values
maxValueToConversionHeight = 4  # Maximum value to express height in meters, so that no conversion is required
removeAttributeAgeOutOfRange = True  # Removes any record that has the age outside the minimum and maximum range

# Remove attributes unnecessary from dataset
attributesDataSet = getAttributesDataSet()

attributesRemove.append(attributesDataSet['HDA2'])
attributesRemove.append(attributesDataSet['PPA'])
attributesRemove.append(attributesDataSet['CONVERNIO'])
attributesRemove.append(attributesDataSet['ANIVERSARIO'])
attributesRemove.append(attributesDataSet['ATENDIMENTO'])
attributesRemove.append(attributesDataSet['ID'])

# Directory containing the original dataset in csv UTF-8
dataSetCSVDirectory = '../DataSet/'

# Original dataset in csv UTF-8
dataSetCSVInput = dataSetCSVDirectory + 'DataSetOriginal.csv'

# Normalized dataset output
dataSetCSVOutput = dataSetCSVDirectory + 'DataSetNormalization.csv'

# Removes output dataset before execution
if os.path.isfile(dataSetCSVOutput):
    os.remove(dataSetCSVOutput)

# Document content CSV original processed
processedDocument = []
normalizeDocument = []

# Read Original DataSet exections functions normalization write DataSet Ouput
normalization = DefsNormalization(maxValueFC, minValueFC, maxValuePA, minValuePA, maxValueIMC, minValueIMC, maxValueAge,
                                  minValueAge, maxValueWeight, minValueWeight, maxValueHeight, minValueHeight,
                                  attributesRemove, missingValuesGenere, maxValueToConversionHeight,
                                  removeAttributeAgeOutOfRange)

# Read and processed original document
firstLine = True
indexInterestClass = 0
with open(dataSetCSVInput, newline='', encoding='utf-8') as csvReaderFile:
    readerCSV = csv.reader(csvReaderFile)

    for row in readerCSV:
        if row[attributesDataSet['NORMALXANORMAL']] != '':
            line = normalization.replaceInvalidInterestArguments(row)
            line = normalization.replaceAccentuationAndUpperCase(line)

            if not firstLine:
                line = normalization.processNORMALXANORMAL(line)
                line = normalization.processIDADE(line)
                line = normalization.processSEXO(line)
                line = normalization.processALTURA(line)
                line = normalization.processPESO(line)
                line = normalization.processIMC(line)
                line = normalization.processFC(line)
                line = normalization.processPAS(line)
                line = normalization.processPAD(line)
                line = normalization.processPPA(line)

            if normalization.validAgeValid(line):
                line = normalization.removeExpendableAttribute(line)

                if firstLine:
                    indexInterestClass = getIndexAttributeClass(line, 'NORMAL X ANORMAL')
                    firstLine = False

                line = normalization.moveLastPositionClass(line, indexInterestClass)
                processedDocument.append(line)

#  Discretize, and merge attributes
firstLine = True
indexClassPESO = -1
indexClassALTURA = -1
indexClassIMC = -1
indexClassIDADE = -1
indexClassPAS = -1
indexClassPAD = -1
indexClassFC = -1
indexClassMOTIVO1 = -1
indexClassMOTIVO2 = -1
with open(dataSetCSVOutput, 'w', newline='', encoding='utf-8') as csvWriterFile:
    writerCSV = csv.writer(csvWriterFile)

    for line in processedDocument:
        if firstLine:
            indexClassPESO = getIndexAttributeClass(line, 'PESO')
            indexClassALTURA = getIndexAttributeClass(line, 'ALTURA')
            indexClassIMC = getIndexAttributeClass(line, 'IMC')
            indexClassIDADE = getIndexAttributeClass(line, 'IDADE')
            indexClassPAS = getIndexAttributeClass(line, 'PA SISTOLICA')
            indexClassPAD = getIndexAttributeClass(line, 'PA DIASTOLICA')
            indexClassFC = getIndexAttributeClass(line, 'FC')
            indexClassMOTIVO1 = getIndexAttributeClass(line, 'MOTIVO1')
            indexClassMOTIVO2 = getIndexAttributeClass(line, 'MOTIVO2')

            line = normalization.mergeMOTIVOS(line, indexClassMOTIVO1, indexClassMOTIVO2)  # remove title MOTIVO2

            firstLine = False
        else:
            line = normalization.discretizeAtribute(line, indexClassPESO, classDiscretizePESO)
            line = normalization.discretizeAtribute(line, indexClassALTURA, classDiscretizeALTURA)
            line = normalization.discretizeAtribute(line, indexClassIMC, classDiscretizeIMC)
            line = normalization.discretizeAtribute(line, indexClassIDADE, classDiscretizeIDADE)
            line = normalization.discretizeAtribute(line, indexClassPAS, classDiscretizePAS)
            line = normalization.discretizeAtribute(line, indexClassPAD, classDiscretizePAD)
            line = normalization.discretizeAtribute(line, indexClassFC, classDiscretizeFC)

            line = normalization.mergeMOTIVOS(line, indexClassMOTIVO1, indexClassMOTIVO2)

        writerCSV.writerow(line)