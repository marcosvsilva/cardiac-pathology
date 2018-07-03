from unicodedata import normalize
from dateutil import parser
from collections import Counter

# Atributes DataSet
atributesDataSet = {'ID': 0, 'PESO': 1, 'ALTURA': 2, 'IMC': 3, 'ATENDIMENTO': 4, 'ANIVERSARIO': 5, 'IDADE': 6,
                    'CONVERNIO': 7, 'PULSO': 8, 'PASISTOLICA': 9, 'PADIASTOLICA': 10, 'PPA': 11, 'NORMALXANORMAL': 12,
                    'B2': 13, 'SOPRO': 14, 'FC': 15, 'HDA1': 16, 'HDA2': 17, 'SEXO': 18, 'REASON1': 19, 'REASON2': 20}

missingValue = ''


def calculateAge(attendance, birthday):
    age = attendance.year - birthday.year
    monthVeri = attendance.month - birthday.month
    dateVeri = attendance.day - birthday.day

    age = int(age)
    monthVeri = int(monthVeri)
    dateVeri = int(dateVeri)

    if monthVeri < 0:
        age = age - 1
    elif dateVeri < 0 and monthVeri == 0:
        age = age - 1

    return age


def checkImc(imc):
    imc = float(imc)
    if imc > 0 or imc <= 60:
        return round(imc, 2)
    else:
        return missingValue


def removeExpendableAttribute(line):
    line.pop(atributesDataSet['CONVERNIO'])
    line.pop(atributesDataSet['ANIVERSARIO'])
    line.pop(atributesDataSet['ATENDIMENTO'])
    line.pop(atributesDataSet['ID'])
    return line


def replaceInvalidArguments(line):
    if '#VALUE!' in line:
        index = line.index('#VALUE!')
        line[index] = missingValue
        replaceInvalidArguments(line)

    if ',' in line:
        index = line.index(',')
        line[index] = '.'
        replaceInvalidArguments(line)
    return line


def replaceAccentuationAndUpperCase(line):
    for i in range(len(line)):
        line[i] = normalize('NFKD', line[i]).encode('ASCII', 'ignore').decode('ASCII')
        line[i] = line[i].upper()
    return line

def moveLastPositionInterestClass(line):
    return moveLastPositionClass(line, atributesDataSet['NORMALXANORMAL'])

def moveLastPositionClass(line, position):
    if position == atributesDataSet.__len__()-1:
        return line
    else:
        aux = line[position]
        line[position] = line[position+1]
        line[position+1] = aux
        return moveLastPositionClass(line, position+1)

def normalizeNORMALXANORMAL(line):
    if line[atributesDataSet['NORMALXANORMAL']] != 'NORMAL X ANORMAL':

        if line[atributesDataSet['NORMALXANORMAL']] in ('NORMAL', 'NORMAIS'):
            line[atributesDataSet['NORMALXANORMAL']] = 'NORMAL'

        elif line[atributesDataSet['NORMALXANORMAL']] in ('ANORMAL'):
            line[atributesDataSet['NORMALXANORMAL']] = 'ANORMAL'

        else:
            line[atributesDataSet['NORMALXANORMAL']] = missingValue

    return line


def normalizeSEXO(line):
    if line[atributesDataSet['SEXO']] != 'SEXO':

        if line[atributesDataSet['SEXO']] in ('M', 'MASCULINO'):
            line[atributesDataSet['SEXO']] = 'MASCULINO'

        elif line[atributesDataSet['SEXO']] in ('F', 'FEMININO'):
            line[atributesDataSet['SEXO']] = 'FEMININO'

        else:
            line[atributesDataSet['SEXO']] = missingValue

    return line


def normalizePESO(line):
    if line[atributesDataSet['PESO']] != 'PESO':
        if line[atributesDataSet['PESO']] == '':
            line[atributesDataSet['PESO']] = missingValue

        elif float(line[atributesDataSet['PESO']]) < 0:
            line[atributesDataSet['PESO']] = missingValue

        elif float(line[atributesDataSet['PESO']]) > 500:
            line[atributesDataSet['PESO']] = missingValue

    return line


def normalizeIDADE(line):
    if line[atributesDataSet['IDADE']] != 'IDADE':
        try:
            attendance = parser.parse(line[atributesDataSet['ATENDIMENTO']])
        except ValueError:
            attendance = None

        try:
            birthday = parser.parse(line[atributesDataSet['ANIVERSARIO']])
        except ValueError:
            birthday = None

        if (attendance != None) and (birthday != None):
            age = calculateAge(attendance, birthday)

            if age >= 0:
                line[atributesDataSet['IDADE']] = age
            else:
                line[atributesDataSet['IDADE']] = missingValue
        else:
            line[atributesDataSet['IDADE']] = missingValue

    return line


def normalizeIMC(line):
    if line[atributesDataSet['IMC']] != 'IMC':
        try:
            height = float(line[atributesDataSet['ALTURA']])
        except ValueError:
            height = 0

        try:
            weight = float(line[atributesDataSet['PESO']])
        except ValueError:
            weight = 0

        if (height > 0) and (weight > 0):
            if height > 4:
                height = height / 100

            imc = weight / (height * height)
            line[atributesDataSet['IMC']] = checkImc(imc)

        elif line[atributesDataSet['IMC']] != missingValue:
            line[atributesDataSet['IMC']] = checkImc(line[atributesDataSet['IMC']])

    return line