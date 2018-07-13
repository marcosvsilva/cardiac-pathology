import csv
import os
from DataSetNormalization.DefsNormalization import DefsNormalization, getAttributesDataSet, getIndexAttributeClass

# Moldable Parameters for Data Normalization

# Max and min values for attributes
maxValueFC = 200
minValueFC = 40

maxValuePA = 200
minValuePA = 50

maxValueIMC = 60.0
minValueIMC = 1.0

maxValueAge = 18
minValueAge = -1

maxValueWeight = 500.0
minValueWeight = 0.1

maxValueHeight = 350
minValueHeight = 1

attributesRemove = []  # Remove attributes unnecessary from dataset
missingValuesGenere = True  # Replaces the UNDEFINED genders with missing values
maxValueToConversionHeight = 4  # Maximum value to express height in meters, so that no conversion is required
removeAttributeAgeOutOfRange = True  # Removes any record that has the age outside the minimum and maximum range

# Remove attributes unnecessary from dataset
attributesDataSet = getAttributesDataSet()

attributesRemove.append(attributesDataSet['HDA2'])
#attributesRemove.append(attributesDataSet['PADIASTOLICA'])
#attributesRemove.append(attributesDataSet['PASISTOLICA'])
attributesRemove.append(attributesDataSet['CONVERNIO'])
attributesRemove.append(attributesDataSet['ANIVERSARIO'])
attributesRemove.append(attributesDataSet['ATENDIMENTO'])
#attributesRemove.append(attributesDataSet['ALTURA'])
#attributesRemove.append(attributesDataSet['IMC'])
#attributesRemove.append(attributesDataSet['PESO'])
attributesRemove.append(attributesDataSet['ID'])

# Directory containing the original dataset in csv UTF-8
dataSetCSVDirectory = '../DataSet/'

# Original dataset in csv UTF-8
dataSetCSVInput = dataSetCSVDirectory + 'DataSet.csv'

# Normalized dataset output
dataSetCSVOutput = dataSetCSVDirectory + 'DataSetNormalization.csv'

# Removes output dataset before execution
if os.path.isfile(dataSetCSVOutput):
    os.remove(dataSetCSVOutput)

# Document content CSV original processed
processedDocument = []

# Read Original DataSet exections functions normalization write DataSet Ouput
normalization = DefsNormalization(maxValueFC, minValueFC, maxValuePA, minValuePA, maxValueIMC, minValueIMC, maxValueAge,
                                  minValueAge, maxValueWeight, minValueWeight, maxValueHeight, minValueHeight,
                                  attributesRemove, missingValuesGenere, maxValueToConversionHeight)

# Processed document
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

            line = normalization.removeExpendableAttribute(line)
            if firstLine:
                indexInterestClass = getIndexAttributeClass(line, 'NORMAL X ANORMAL')
                firstLine = False

            line = normalization.moveLastPositionClass(line, indexInterestClass)
            processedDocument.append(line)

#  Process and normalize attributes
firstLine = True
indexClassFC = 0
indexClassIMC = 0
indexClassIDADE = 0
indexClassALTURA = 0
with open(dataSetCSVOutput, 'w', newline='', encoding='utf-8') as csvWriterFile:
    writerCSV = csv.writer(csvWriterFile)

    for line in processedDocument:
        if firstLine:
            indexClassFC = getIndexAttributeClass(line, 'FC')
            indexClassIMC = getIndexAttributeClass(line, 'IMC')
            indexClassIDADE = getIndexAttributeClass(line, 'IDADE')
            indexClassALTURA = getIndexAttributeClass(line, 'ALTURA')
            writerCSV.writerow(line)
            firstLine = False
        else:
            '''
            line = normalization.normalizeattribute(line, indexClassFC, normalization.minValueNormalizationFC,
                                                    normalization.maxValueNormalizationFC)     
                                                       
            line = normalization.normalizeattribute(line, indexClassIMC, normalization.minValueNormalizationIMC,
                                                    normalization.maxValueNormalizationIMC)

            line = normalization.normalizeattribute(line, indexClassIDADE, normalization.minValueNormalizationIDADE,
                                                    normalization.maxValueNormalizationIDADE)            

            line = normalization.normalizeattribute(line, indexClassALTURA, normalization.minValueNormalizationALTURA,
                                                    normalization.maxValueNormalizationALTURA)
            '''

            if removeAttributeAgeOutOfRange:
                if line[indexClassIDADE] != '':
                    if minValueAge < line[indexClassIDADE] <= maxValueAge:
                        writerCSV.writerow(line)
            else:
                writerCSV.writerow(line)