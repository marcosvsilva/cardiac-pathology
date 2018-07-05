from unicodedata import normalize
from dateutil import parser

# Atributes DataSet
attributesDataSet = {'ID': 0, 'PESO': 1, 'ALTURA': 2, 'IMC': 3, 'ATENDIMENTO': 4, 'ANIVERSARIO': 5, 'IDADE': 6,
                     'CONVERNIO': 7, 'PULSO': 8, 'PASISTOLICA': 9, 'PADIASTOLICA': 10, 'PPA': 11, 'NORMALXANORMAL': 12,
                     'B2': 13, 'SOPRO': 14, 'FC': 15, 'HDA1': 16, 'HDA2': 17, 'SEXO': 18, 'REASON1': 19, 'REASON2': 20}

convertHeightMTOCM = 100

missingValue = ''


def getAttributesDataSet():
    return attributesDataSet


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

    if minValue < imc <= maxValue:
        return round(imc, 2)
    else:
        return missingValue

def checkPPA(ppa):
    ppaNew = missingValue
    if ppa != '':
        if ppa in ['NORMAL']:
            ppaNew = 'NORMAL'

        if ppa in ['PRE-HIPERTENSAO PAS', 'PRE-HIPERTENSAO PAD']:
            ppaNew = 'PRE-HIPERTENSAO'

        if ppa in ['HAS-1 PAS', 'HAS-1 PAD']:
            ppaNew = 'HIPERTENSAO ESTAGIO 1'

        if ppa in ['HAS-2 PAS', 'HAS-2 PAD']:
            ppaNew = 'HIPERTENSAO ESTAGIO 2'

        if ppa in ['HAS-3 PAS', 'HAS-3 PAD']:
            ppaNew = 'HIPERTENSAO ESTAGIO 3'

    return ppaNew

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
    if position == line.__len__() - 1:
        return line
    else:
        aux = line[position]
        line[position] = line[position + 1]
        line[position + 1] = aux
        return moveLastPositionClass(line, position + 1)


class DefsNormalization:
    maxValueFC = 0
    minValueFC = 0
    maxValuePA = 0
    minValuePA = 0
    maxValueIMC = 0
    minValueIMC = 0
    maxValueAge = 0
    minValueAge = 0
    maxValueWeight = 0
    minValueWeight = 0
    maxValueHeight = 0
    minValueHeight = 0
    attributesRemove = []
    missingValuesGenere = False
    maxValueToConversionHeight = 0

    def __init__(self, maxValueFC, minValueFC, maxValuePA, minValuePA, maxValueIMC, minValueIMC, maxValueAge,
                 minValueAge, maxValueWeight, minValueWeight, maxValueHeight, minValueHeight, attributesRemove,
                 missingValuesGenere, maxValueToConversionHeight):
        self.maxValueFC = maxValueFC
        self.minValueFC = minValueFC
        self.maxValuePA = maxValuePA
        self.minValuePA = minValuePA
        self.maxValueIMC = maxValueIMC
        self.minValueIMC = minValueIMC
        self.maxValueAge = maxValueAge
        self.minValueAge = minValueAge
        self.maxValueWeight = maxValueWeight
        self.minValueWeight = minValueWeight
        self.maxValueHeight = maxValueHeight
        self.minValueHeight = minValueHeight
        self.attributesRemove = attributesRemove
        self.missingValuesGenere = missingValuesGenere
        self.maxValueToConversionHeight = maxValueToConversionHeight

    def removeExpendableAttribute(self, line):
        for index in self.attributesRemove:
            line.pop(index)
        return line

    def replaceInvalidInterestArguments(self, line):
        return replaceInvalidArguments(line)

    def moveLastPositionInterestClass(self, line, index):
        return moveLastPositionClass(line, index)

    def replaceAccentuationAndUpperCase(self, line):
        for i in range(len(line)):
            line[i] = normalize('NFKD', line[i]).encode('ASCII', 'ignore').decode('ASCII')
            line[i] = line[i].upper()

        return line

    def normalizeNORMALXANORMAL(self, line):
        if line[attributesDataSet['NORMALXANORMAL']] != 'NORMAL X ANORMAL':
            if line[attributesDataSet['NORMALXANORMAL']] in ('NORMAL', 'NORMAIS'):
                line[attributesDataSet['NORMALXANORMAL']] = 'NORMAL'

            elif line[attributesDataSet['NORMALXANORMAL']] in ('ANORMAL'):
                line[attributesDataSet['NORMALXANORMAL']] = 'ANORMAL'

            else:
                line[attributesDataSet['NORMALXANORMAL']] = missingValue

        return line

    def normalizeSEXO(self, line):
        if line[attributesDataSet['SEXO']] != 'SEXO':
            if line[attributesDataSet['SEXO']] == missingValue:
                line[attributesDataSet['SEXO']] = missingValue

            elif line[attributesDataSet['SEXO']] in ('M', 'MASCULINO'):
                line[attributesDataSet['SEXO']] = 'MASCULINO'

            elif line[attributesDataSet['SEXO']] in ('F', 'FEMININO'):
                line[attributesDataSet['SEXO']] = 'FEMININO'

            elif line[attributesDataSet['SEXO']] in ('INDETERMINADO'):
                if self.missingValuesGenere:
                    line[attributesDataSet['SEXO']] = missingValue
                else:
                    line[attributesDataSet['SEXO']] = 'INDETERMINADO'

        return line

    def normalizeIDADE(self, line):
        if line[attributesDataSet['IDADE']] != 'IDADE':
            try:
                attendance = parser.parse(line[attributesDataSet['ATENDIMENTO']])
            except ValueError:
                attendance = None

            try:
                birthday = parser.parse(line[attributesDataSet['ANIVERSARIO']])
            except ValueError:
                birthday = None

            if (attendance is not None) and (birthday is not None):
                age = calculateAge(attendance, birthday)

                if age >= 0:
                    line[attributesDataSet['IDADE']] = age
                else:
                    line[attributesDataSet['IDADE']] = missingValue
            else:
                line[attributesDataSet['IDADE']] = missingValue

        return line

    def normalizePPA(self, line):
        if line[attributesDataSet['PPA']] != 'PPA':
            try:
                pas = int(line[attributesDataSet['PASISTOLICA']])
            except ValueError:
                pas = 0

            try:
                pad = int(line[attributesDataSet['PADIASTOLICA']])
            except ValueError:
                pad = 0

            minPA = int(self.minValuePA)
            maxPA = int(self.maxValuePA)

            line[attributesDataSet['PPA']] = checkPPA(line[attributesDataSet['PPA']])
            if minPA < pas <= maxPA:
                if minPA < pad <= maxPA:
                    if pas <= 120 and pad <= 80:
                        line[attributesDataSet['PPA']] = 'NORMAL'

                    if 120 < pas < 140 or 80 < pad < 90:
                        line[attributesDataSet['PPA']] = 'PRE-HIPERTENSAO'

                    if 140 <= pas < 160 or 90 <= pad < 100:
                        line[attributesDataSet['PPA']] = 'HIPERTENSAO ESTAGIO 1'

                    if 160 <= pas < 180 or 100 <= pad < 110:
                        line[attributesDataSet['PPA']] = 'HIPERTENSAO ESTAGIO 2'

                    if pas >= 180 or pad >= 110:
                        line[attributesDataSet['PPA']] = 'HIPERTENSAO ESTAGIO 3'

        return line

    def normalizePESO(self, line):
        if line[attributesDataSet['PESO']] != 'PESO':
            if line[attributesDataSet['PESO']] == '':
                line[attributesDataSet['PESO']] = missingValue

            elif float(line[attributesDataSet['PESO']]) <= self.minValueWeight:
                line[attributesDataSet['PESO']] = missingValue

            elif float(line[attributesDataSet['PESO']]) > self.maxValueWeight:
                line[attributesDataSet['PESO']] = missingValue

        return line

    def normalizeALTURA(self, line):
        if line[attributesDataSet['ALTURA']] != 'ALTURA':
            if line[attributesDataSet['ALTURA']] == '':
                line[attributesDataSet['ALTURA']] = missingValue

            elif float(line[attributesDataSet['ALTURA']]) <= self.minValueHeight:
                line[attributesDataSet['ALTURA']] = missingValue

            elif float(line[attributesDataSet['ALTURA']]) > self.maxValueHeight:
                line[attributesDataSet['ALTURA']] = missingValue

        return line

    def normalizeIMC(self, line):
        if line[attributesDataSet['IMC']] != 'IMC':
            try:
                line = self.normalizeALTURA(line)
                height = float(line[attributesDataSet['ALTURA']])
            except ValueError:
                height = 0

            try:
                line = self.normalizePESO(line)
                weight = float(line[attributesDataSet['PESO']])
            except ValueError:
                weight = 0

            if (height > 0) and (weight > 0):
                if height > self.maxValueToConversionHeight:
                    height = height / convertHeightMTOCM

                imc = weight / (height * height)
                line[attributesDataSet['IMC']] = checkImc(imc, self.maxValueIMC, self.minValueIMC)

            elif line[attributesDataSet['IMC']] != missingValue:
                line[attributesDataSet['IMC']] = checkImc(line[attributesDataSet['IMC']], self.maxValueIMC,
                                                          self.minValueIMC)

        return line

    def normalizeFC(self, line):
        if line[attributesDataSet['FC']] != 'FC':
            if line[attributesDataSet['FC']] == '':
                line[attributesDataSet['FC']] = missingValue
            else:
                try:
                    intFC = int(line[attributesDataSet['FC']])

                    if self.minValueFC < intFC <= self.maxValueFC:
                        line[attributesDataSet['FC']] = int(line[attributesDataSet['FC']])
                    else:
                        line[attributesDataSet['FC']] = missingValue

                except ValueError:
                    line[attributesDataSet['FC']] = missingValue

        return line
