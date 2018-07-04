from unicodedata import normalize
from dateutil import parser

# Atributes DataSet
atributesDataSet = {'ID': 0, 'PESO': 1, 'ALTURA': 2, 'IMC': 3, 'ATENDIMENTO': 4, 'ANIVERSARIO': 5, 'IDADE': 6,
                    'CONVERNIO': 7, 'PULSO': 8, 'PASISTOLICA': 9, 'PADIASTOLICA': 10, 'PPA': 11, 'NORMALXANORMAL': 12,
                    'B2': 13, 'SOPRO': 14, 'FC': 15, 'HDA1': 16, 'HDA2': 17, 'SEXO': 18, 'REASON1': 19, 'REASON2': 20}

convertHeightMTOCM = 100

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


def checkImc(imc, maxValueIMC, minValueIMC):
    imc = float(imc)
    maxValue = float(maxValueIMC)
    minValue = float(minValueIMC)

    if imc > minValue and imc <= maxValue:
        return round(imc, 2)
    else:
        return missingValue


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


def moveLastPositionClass(line, position):
    if position == atributesDataSet.__len__() - 1:
        return line
    else:
        aux = line[position]
        line[position] = line[position + 1]
        line[position + 1] = aux
        return moveLastPositionClass(line, position + 1)


class DefsNormalization:
    maxValueFC = 0
    minValueFC = 0
    maxValueIMC = 0
    minValueIMC = 0
    maxValueAge = 0
    minValueAge = 0
    maxValueWeight = 0
    minValueWeight = 0
    maxValueHeight = 0
    minValueHeight = 0
    removePAS = False
    removeAlturaAndPeso = False
    missingValuesGenere = False
    maxValueToConversionHeight = 0

    def __init__(self, maxValueFC, minValueFC, maxValueIMC, minValueIMC, maxValueAge, minValueAge, maxValueWeight,
                 minValueWeight, maxValueHeight, minValueHeight, removePAS, removeAlturaAndPeso, missingValuesGenere,
                 maxValueToConversionHeight):
        self.maxValueFC = maxValueFC
        self.minValueFC = minValueFC
        self.maxValueIMC = maxValueIMC
        self.minValueIMC = minValueIMC
        self.maxValueAge = maxValueAge
        self.minValueAge = minValueAge
        self.maxValueWeight = maxValueWeight
        self.minValueWeight = minValueWeight
        self.maxValueHeight = maxValueHeight
        self.minValueHeight = minValueHeight
        self.removePAS = removePAS
        self.removeAlturaAndPeso = removeAlturaAndPeso
        self.missingValuesGenere = missingValuesGenere
        self.maxValueToConversionHeight = maxValueToConversionHeight

    def removeExpendableAttribute(self, line):
        if self.removePAS:
            line.pop(atributesDataSet['PADIASTOLICA'])
            line.pop(atributesDataSet['PASISTOLICA'])

        line.pop(atributesDataSet['CONVERNIO'])
        line.pop(atributesDataSet['ANIVERSARIO'])
        line.pop(atributesDataSet['ATENDIMENTO'])

        if self.removeAlturaAndPeso:
            line.pop(atributesDataSet['ALTURA'])
            line.pop(atributesDataSet['PESO'])

        line.pop(atributesDataSet['ID'])
        return line

    def replaceInvalidInterestArguments(self, line):
        return replaceInvalidArguments(line)

    def moveLastPositionInterestClass(self, line):
        return moveLastPositionClass(line, atributesDataSet['NORMALXANORMAL'])

    def replaceAccentuationAndUpperCase(self, line):
        for i in range(len(line)):
            line[i] = normalize('NFKD', line[i]).encode('ASCII', 'ignore').decode('ASCII')
            line[i] = line[i].upper()

        return line

    def normalizeNORMALXANORMAL(self, line):
        if line[atributesDataSet['NORMALXANORMAL']] != 'NORMAL X ANORMAL':
            if line[atributesDataSet['NORMALXANORMAL']] in ('NORMAL', 'NORMAIS'):
                line[atributesDataSet['NORMALXANORMAL']] = 'NORMAL'

            elif line[atributesDataSet['NORMALXANORMAL']] in ('ANORMAL'):
                line[atributesDataSet['NORMALXANORMAL']] = 'ANORMAL'

            else:
                line[atributesDataSet['NORMALXANORMAL']] = missingValue

        return line

    def normalizeSEXO(self, line):
        if line[atributesDataSet['SEXO']] != 'SEXO':
            if line[atributesDataSet['SEXO']] == missingValue:
                line[atributesDataSet['SEXO']] = missingValue

            elif line[atributesDataSet['SEXO']] in ('M', 'MASCULINO'):
                line[atributesDataSet['SEXO']] = 'MASCULINO'

            elif line[atributesDataSet['SEXO']] in ('F', 'FEMININO'):
                line[atributesDataSet['SEXO']] = 'FEMININO'

            elif line[atributesDataSet['SEXO']] in ('INDETERMINADO'):
                if self.missingValuesGenere:
                    line[atributesDataSet['SEXO']] = missingValue
                else:
                    line[atributesDataSet['SEXO']] = 'INDETERMINADO'

        return line

    def normalizeIDADE(self, line):
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

    def normalizePESO(self, line):
        if line[atributesDataSet['PESO']] != 'PESO':
            if line[atributesDataSet['PESO']] == '':
                line[atributesDataSet['PESO']] = missingValue

            elif float(line[atributesDataSet['PESO']]) <= self.minValueWeight:
                line[atributesDataSet['PESO']] = missingValue

            elif float(line[atributesDataSet['PESO']]) > self.maxValueWeight:
                line[atributesDataSet['PESO']] = missingValue

        return line

    def normalizeALTURA(self, line):
        if line[atributesDataSet['ALTURA']] != 'ALTURA':
            if line[atributesDataSet['ALTURA']] == '':
                line[atributesDataSet['ALTURA']] = missingValue

            elif float(line[atributesDataSet['ALTURA']]) <= self.minValueHeight:
                line[atributesDataSet['ALTURA']] = missingValue

            elif float(line[atributesDataSet['ALTURA']]) > self.maxValueHeight:
                line[atributesDataSet['ALTURA']] = missingValue

        return line

    def normalizeIMC(self, line):
        if line[atributesDataSet['IMC']] != 'IMC':
            try:
                line = self.normalizeALTURA(line)
                height = float(line[atributesDataSet['ALTURA']])
            except ValueError:
                height = 0

            try:
                line = self.normalizePESO(line)
                weight = float(line[atributesDataSet['PESO']])
            except ValueError:
                weight = 0

            if (height > 0) and (weight > 0):
                if height > self.maxValueToConversionHeight:
                    height = height / convertHeightMTOCM

                imc = weight / (height * height)
                line[atributesDataSet['IMC']] = checkImc(imc, self.maxValueIMC, self.minValueIMC)

            elif line[atributesDataSet['IMC']] != missingValue:
                line[atributesDataSet['IMC']] = checkImc(line[atributesDataSet['IMC']], self.maxValueIMC,
                                                         self.minValueIMC)

        return line

    def normalizeFC(self, line):
        if line[atributesDataSet['FC']] != 'FC':
            if line[atributesDataSet['FC']] == '':
                line[atributesDataSet['FC']] = missingValue
            else:
                try:
                    intFC = int(line[atributesDataSet['FC']])

                    if intFC > self.minValueFC and intFC <= self.maxValueFC:
                        line[atributesDataSet['FC']] = int(line[atributesDataSet['FC']])
                    else:
                        line[atributesDataSet['FC']] = missingValue

                except ValueError:
                    line[atributesDataSet['FC']] = missingValue

        return line
