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


def getIndexAttributeClass(line, attribute):
    for i in range(len(line)):
        if line[i] == attribute:
            return i


def calculateAge(attendance, birthday):
    age = -1
    try:
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
    except ValueError:
        age = -1

    return age


def checkImc(imc, maxValueIMC, minValueIMC):
    try:
        imc = float(imc)
        maxValue = float(maxValueIMC)
        minValue = float(minValueIMC)

        if minValue <= imc <= maxValue:
            imc = round(imc, 2)
        else:
            imc = -1

    except ValueError:
        imc = -1

    return imc


def checkPPA(ppa):
    ppaNew = missingValue
    if ppa != '':
        if ppa in ['NORMAL']:
            ppaNew = 'NORMAL'

        if ppa in ['PRE-HIPERTENSAO PAS', 'PRE-HIPERTENSAO PAD', 'HAS-1 PAS', 'HAS-1 PAD', 'HAS-3 PAS', 'HAS-3 PAD']:
            ppaNew = 'HAS'

    return ppaNew


def calculeOneYearPPA(pas, pad, height, genere):
    pas = int(pas)
    pad = int(pad)
    height = int(height)
    male = (genere == 'MASCULINO')

    ppaNew = missingValue
    if male:
        if pas > 0 and pad > 0:
            if 5 <= height < 10:
                if pa < 80:
                    ppaNew = 'HIPOTENSAO'

    return ppaNew


def replaceInvalidInterestArgumentsRecursive(line):
    if '#VALUE!' in line:
        index = line.index('#VALUE!')
        line[index] = missingValue
        replaceInvalidInterestArgumentsRecursive(line)

    if ',' in line:
        index = line.index(',')
        line[index] = '.'
        replaceInvalidInterestArgumentsRecursive(line)

    return line


def moveLastPositionClassRecursive(line, position):
    if position == line.__len__() - 1:
        return line
    else:
        aux = line[position]
        line[position] = line[position + 1]
        line[position + 1] = aux
        return moveLastPositionClassRecursive(line, position + 1)


class DefsNormalization:
    # values for processing
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

    # values for normalization
    maxValueNormalizationFC = 0
    minValueNormalizationFC = 0
    maxValueNormalizationIMC = 0
    minValueNormalizationIMC = 0
    maxValueNormalizationIDADE = 0
    minValueNormalizationIDADE = 0
    maxValueNormalizationALTURA = 0
    minValueNormalizationALTURA = 0

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

        # Assigned minimum values with the maximum values so that they are always greater than the minimum values
        self.minValueNormalizationFC = maxValueFC
        self.minValueNormalizationIMC = maxValueIMC
        self.minValueNormalizationIDADE = maxValueAge
        self.minValueNormalizationALTURA = maxValueHeight

    def removeExpendableAttribute(self, line):
        for index in self.attributesRemove:
            line.pop(index)
        return line

    def replaceInvalidInterestArguments(self, line):
        return replaceInvalidInterestArgumentsRecursive(line)

    def moveLastPositionClass(self, line, index):
        return moveLastPositionClassRecursive(line, index)

    def processNORMALXANORMAL(self, line):
        if line[attributesDataSet['NORMALXANORMAL']] != 'NORMAL X ANORMAL':
            if line[attributesDataSet['NORMALXANORMAL']] in ('NORMAL', 'NORMAIS'):
                line[attributesDataSet['NORMALXANORMAL']] = 'NORMAL'

            elif line[attributesDataSet['NORMALXANORMAL']] in ('ANORMAL'):
                line[attributesDataSet['NORMALXANORMAL']] = 'ANORMAL'

            else:
                line[attributesDataSet['NORMALXANORMAL']] = missingValue

        return line

    def replaceAccentuationAndUpperCase(self, line):
        for i in range(len(line)):
            line[i] = normalize('NFKD', line[i]).encode('ASCII', 'ignore').decode('ASCII')
            line[i] = line[i].upper()

        return line

    def processSEXO(self, line):
        if line[attributesDataSet['SEXO']] != 'SEXO':
            if line[attributesDataSet['SEXO']] in ('M', 'MASCULINO'):
                line[attributesDataSet['SEXO']] = 'MASCULINO'

            elif line[attributesDataSet['SEXO']] in ('F', 'FEMININO'):
                line[attributesDataSet['SEXO']] = 'FEMININO'

            elif line[attributesDataSet['SEXO']] in ('INDETERMINADO'):
                if self.missingValuesGenere:
                    line[attributesDataSet['SEXO']] = missingValue
                else:
                    line[attributesDataSet['SEXO']] = 'INDETERMINADO'

        return line

    def processIDADE(self, line):
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

                if self.minValueAge <= age <= self.maxValueAge:
                    line[attributesDataSet['IDADE']] = age

                    if age < self.minValueNormalizationIDADE:
                        self.minValueNormalizationIDADE = age

                    if age > self.maxValueNormalizationIDADE:
                        self.maxValueNormalizationIDADE = age
                else:
                    line[attributesDataSet['IDADE']] = missingValue
            else:
                line[attributesDataSet['IDADE']] = missingValue

        return line

    def processPAS(self, line):
        if line[attributesDataSet['PASISTOLICA']] != 'PA SISTOLICA':
            try:
                pas = int(line[attributesDataSet['PASISTOLICA']])
            except ValueError:
                pas = 0

            if self.minValuePA <= pas < self.maxValuePA:
                line[attributesDataSet['PASISTOLICA']] = pas
            else:
                line[attributesDataSet['PASISTOLICA']] = missingValue

        return line

    def processPAD(self, line):
        if line[attributesDataSet['PADIASTOLICA']] != 'PA DIASTOLICA':
            try:
                pad = int(line[attributesDataSet['PADIASTOLICA']])
            except ValueError:
                pad = 0

            if self.minValuePA <= pad < self.maxValuePA:
                line[attributesDataSet['PADIASTOLICA']] = pad
            else:
                line[attributesDataSet['PADIASTOLICA']] = missingValue

        return line

    def processPPA(self, line):
        if line[attributesDataSet['PPA']] != 'PPA':
            line = self.processPAD(line)
            line = self.processPAS(line)

            line[attributesDataSet['PPA']] = checkPPA(line[attributesDataSet['PPA']])
        return line

    def processPESO(self, line):
        if line[attributesDataSet['PESO']] != 'PESO':
            if line[attributesDataSet['PESO']] != missingValue:
                try:
                    weight = float(line[attributesDataSet['PESO']])

                    if self.minValueWeight <= weight <= self.maxValueWeight:
                        line[attributesDataSet['PESO']] = weight
                    else:
                        line[attributesDataSet['PESO']] = missingValue

                except ValueError:
                    line[attributesDataSet['PESO']] = missingValue

        return line

    def processALTURA(self, line):
        if line[attributesDataSet['ALTURA']] != 'ALTURA':
            height = 0
            try:
                if line[attributesDataSet['ALTURA']] != '':
                    heightAux = int(line[attributesDataSet['ALTURA']])

                    if self.minValueHeight <= heightAux <= self.maxValueHeight:
                        height = heightAux
                        line[attributesDataSet['ALTURA']] = height
                    else:
                        line[attributesDataSet['ALTURA']] = missingValue

            except ValueError:
                line[attributesDataSet['ALTURA']] = missingValue
                height = 0

            if height > 0:
                if height < self.minValueNormalizationALTURA:
                    self.minValueNormalizationALTURA = height

                if height > self.maxValueNormalizationALTURA:
                    self.maxValueNormalizationALTURA = height

        return line

    def processIMC(self, line):
        if line[attributesDataSet['IMC']] != 'IMC':
            try:
                line = self.processALTURA(line)
                height = float(line[attributesDataSet['ALTURA']])
            except ValueError:
                height = 0

            try:
                line = self.processPESO(line)
                weight = float(line[attributesDataSet['PESO']])
            except ValueError:
                weight = 0

            imc = -1
            if (height > 0) and (weight > 0):
                if height > self.maxValueToConversionHeight:
                    height = height / convertHeightMTOCM

                imc = weight / (height * height)
                imc = checkImc(imc, self.maxValueIMC, self.minValueIMC)

                if imc > 0:
                    line[attributesDataSet['IMC']] = imc
                else:
                    line[attributesDataSet['IMC']] = missingValue

            elif line[attributesDataSet['IMC']] != missingValue:
                imc = checkImc(line[attributesDataSet['IMC']], self.maxValueIMC, self.minValueIMC)

                if imc > 0:
                    line[attributesDataSet['IMC']] = imc
                else:
                    line[attributesDataSet['IMC']] = missingValue

            if imc > 0:
                if imc < self.minValueNormalizationIMC:
                    self.minValueNormalizationIMC = imc

                if imc > self.maxValueNormalizationIMC:
                    self.maxValueNormalizationIMC = imc

        return line

    def processFC(self, line):
        if line[attributesDataSet['FC']] != 'FC':
            if line[attributesDataSet['FC']] != '':
                try:
                    intFC = int(line[attributesDataSet['FC']])

                    if self.minValueFC <= intFC <= self.maxValueFC:
                        line[attributesDataSet['FC']] = intFC

                        if intFC < self.minValueNormalizationFC:
                            self.minValueNormalizationFC = intFC

                        if intFC > self.maxValueNormalizationFC:
                            self.maxValueNormalizationFC = intFC
                    else:
                        line[attributesDataSet['FC']] = missingValue

                except ValueError:
                    line[attributesDataSet['FC']] = missingValue

        return line

    def normalizeattribute(self, line, indexAttribute, minAttribute, maxAttribute):
        valueAttribute = line[indexAttribute]

        if valueAttribute != missingValue:
            minAttribute = float(minAttribute)
            maxAttribute = float(maxAttribute)
            valueAttribute = float(valueAttribute)
            line[indexAttribute] = round((valueAttribute - minAttribute) / (maxAttribute - minAttribute), 4)
        return line
