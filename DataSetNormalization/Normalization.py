import csv
import os
from unicodedata import normalize
from dateutil import parser
from datetime import datetime

# Directory containing the original dataset in csv UTF-8
dataSetCSVDirectory = '../DataSet/'

# Original dataset in csv UTF-8
dataSetCSVInput = dataSetCSVDirectory + 'DataSet.csv'

# Normalized dataset output
dataSetCSVOutput = dataSetCSVDirectory + 'DataSetNormalization.csv'

# Atributes DataSet
atributesDataSet = {'PESO': 0, 'ALTURA': 1, 'IMC': 2, 'ATENDIMENTO': 3, 'ANIVERSARIO': 4, 'IDADE': 5, 'PULSO': 6,
                    'PASISTOLICA': 7, 'PADIASTOLICA': 7, 'PPA': 9, 'NORMALXANORMAL': 10, 'B2': 11, 'SOPRO': 12,
                    'FC': 13, 'HDA1': 14, 'HDA2': 15, 'SEXO': 16, 'REASON1': 17, 'REASON2': 18}


# Remove Attributes: ID[0] and Convenio[7], Because they are not relevant to the context
def removeExpendableAttributes(line):
    line.pop(7)
    line.pop(0)
    return line


# Clearing invalid data set terms
def replaceInvalidArguments(line):
    if '#VALUE!' in line:
        index = line.index('#VALUE!')
        line[index] = ''
        replaceInvalidArguments(line)

    if ',' in line:
        index = line.index(',')
        line[index] = '.'
        replaceInvalidArguments(line)
    return line


# Removes accent and transforms into uppercase string
def replaceAccentuationAndUpperCase(line):
    for i in range(len(line)):
        line[i] = normalize('NFKD', line[i]).encode('ASCII', 'ignore').decode('ASCII')
        line[i] = line[i].upper()
    return line


# Normalize SEXO
def normalizeSEXO(line):
    if line[atributesDataSet['SEXO']] != 'SEXO':

        if line[atributesDataSet['SEXO']] in ('M', 'MASCULINO'):
            line[atributesDataSet['SEXO']] = 'MASCULINO'

        elif line[atributesDataSet['SEXO']] in ('F', 'FEMININO'):
            line[atributesDataSet['SEXO']] = 'FEMININO'

        else:
            line[atributesDataSet['SEXO']] = 'INDETERMINADO'

    return line

# Normalize PESO
def normalizePESO(line):
    if line[atributesDataSet['PESO']] != 'PESO':
        if line[atributesDataSet['PESO']] == '':
            line[atributesDataSet['PESO']] = 0.0

        elif float(line[atributesDataSet['PESO']]) < 0:
            line[atributesDataSet['PESO']] = 0.0

        elif float(line[atributesDataSet['PESO']]) > 500:
            line[atributesDataSet['PESO']] = 0.0

    return line

def normalizeDATE(date):
    date = parser.parse(date)
    return date.strftime("%Y-%m-%d")

def normalizeDATEORDINAL(date):
    date = datetime.fromordinal(date)
    return date.strftime("%Y-%m-%d")

# Normalize ATENDIMENTO
def normalizeATENDIMENTO(line):
    if line[atributesDataSet['ATENDIMENTO']] != 'ATENDIMENTO':
        try:
            line[atributesDataSet['ATENDIMENTO']] = normalizeDATE(line[atributesDataSet['ATENDIMENTO']])
        except ValueError:
            line[atributesDataSet['ATENDIMENTO']] = ''
    return line

# Normalize dn
def normalizeANIVERSARIO(line):
    if line[atributesDataSet['ANIVERSARIO']] != 'DN':
        try:
            line[atributesDataSet['ANIVERSARIO']] = normalizeDATE(line[atributesDataSet['ANIVERSARIO']])
        except ValueError:
            line[atributesDataSet['ANIVERSARIO']] = ''
    return line

# Removes output dataset before execution
if os.path.isfile(dataSetCSVOutput):
    os.remove(dataSetCSVOutput)

# Read Original DataSet exections functions normalization write DataSet Ouput
with open(dataSetCSVOutput, 'w', newline='', encoding='utf-8') as csvWriterFile:
    writerCSV = csv.writer(csvWriterFile)

    with open(dataSetCSVInput, newline='', encoding='utf-8') as csvReaderFile:
        readerCSV = csv.reader(csvReaderFile)

        for row in readerCSV:
            line = removeExpendableAttributes(row)
            line = replaceInvalidArguments(line)
            line = replaceAccentuationAndUpperCase(line)

            line = normalizeSEXO(line)
            line = normalizePESO(line)
            line = normalizeATENDIMENTO(line)
            line = normalizeANIVERSARIO(line)

            writerCSV.writerow(line)
