# Classification of PPA
normal = 'NORMAL'
hypertension = 'HAS'
missingValue = ''

genereBoy = 'MASCULINO'
genereGirl = 'FEMININO'

indexValueHeight = 'HEIGHT'
indexValuePPA = 'PPA'
indexValuePPD = 'PPD'


def createValue(height, valueMinPPA, valueMinPPD, valuePPA, valuePPD):
    value = None

    if height > 0 and valuePPA > valueMinPPA and valuePPD > valueMinPPD:
        value = {indexValueHeight: height, indexValuePPA: valuePPA, indexValuePPD: valuePPD}

    return value


def classify(value, maxPAS, maxPAD):
    result = missingValue

    if value[indexValuePPA] >= maxPAS or value[indexValuePPD] >= maxPAD:
        result = hypertension
    else:
        result = normal

    return result


def classifyPPA(value, intervalMaxPAS, intervalMaxPAD):
    result = missingValue
    index = -1;

    if value[indexValueHeight] <= 5:
        index = 0

    if 5 < value[indexValueHeight] <= 10:
        index = 1

    if 10 < value[indexValueHeight] <= 25:
        index = 2

    if 25 < value[indexValueHeight] <= 50:
        index = 3

    if 50 < value[indexValueHeight] <= 75:
        index = 4

    if 75 < value[indexValueHeight] <= 90:
        index = 5

    if value[indexValueHeight] > 90:
        index = 6

    if index >= 0:
        result = classify(value, intervalMaxPAS[index], intervalMaxPAD[index])

    return result


class DefsNormalizationPPA:
    value = None
    valueMinPPA = 0
    valueMinPPD = 0

    def __init__(self, valueMinPPA, valueMinPPD):
        self.valueMinPPA = valueMinPPA
        self.valueMinPPD = valueMinPPD

    def ppaCalculate(self, genere, age, height, pas, pad):
        result = missingValue

        if genere != missingValue:
            value = createValue(height, self.valueMinPPD, self.valueMinPPA, pas, pad)

            if value is not None:
                self.value = value
                result = self.ppaCalculateList(age, genere)

        return result

    def ppaCalculateList(self, age, genere):
        result = missingValue

        if age in [0, 1]:
            result = self.ppaCalculeOneYear(genere)
        elif age == 2:
            result = self.ppaCalculeTwoYear(genere)
        elif age == 3:
            result = self.ppaCalculeThreeYear(genere)
        elif age == 4:
            result = self.ppaCalculeFourYear(genere)
        elif age == 5:
            result = self.ppaCalculeFiveYear(genere)
        elif age == 6:
            result = self.ppaCalculeSixYear(genere)
        elif age == 7:
            result = self.ppaCalculeSevenYear(genere)
        elif age == 8:
            result = self.ppaCalculeEightYear(genere)
        elif age == 9:
            result = self.ppaCalculeNineYear(genere)
        elif age == 10:
            result = self.ppaCalculeTenYear(genere)
        elif age == 11:
            result = self.ppaCalculeElevenYear(genere)
        elif age == 12:
            result = self.ppaCalculeTwelveYear(genere)
        elif age == 13:
            result = self.ppaCalculeThirteenYear(genere)
        elif age == 14:
            result = self.ppaCalculeFourteenYear(genere)
        elif age == 15:
            result = self.ppaCalculeFifteenYear(genere)
        elif age == 16:
            result = self.ppaCalculeSixteenYear(genere)
        elif age == 17:
            result = self.ppaCalculeSeventeenYear(genere)
        else:
            result = self.ppaCalculeEighteenYear()

        return result

    #  Classification
    def ppaCalculeOneYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [98, 99, 101, 103, 104, 106, 106]
            intervalMaxPAD = [54, 54, 55, 56, 57, 58, 58]

        if genere == genereGirl:
            intervalMaxPAS = [100, 101, 102, 104, 105, 106, 107]
            intervalMaxPAD = [56, 57, 57, 58, 59, 59, 60]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeTwoYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [101, 102, 104, 106, 108, 109, 110]
            intervalMaxPAD = [59, 59, 60, 61, 62, 63, 63]

        if genere == genereGirl:
            intervalMaxPAS = [102, 103, 104, 105, 107, 108, 109]
            intervalMaxPAD = [61, 62, 62, 63, 64, 65, 65]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeThreeYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [104, 105, 107, 109, 110, 112, 113]
            intervalMaxPAD = [63, 63, 64, 65, 66, 67, 67]

        if genere == genereGirl:
            intervalMaxPAS = [104, 104, 105, 107, 108, 109, 110]
            intervalMaxPAD = [65, 66, 66, 67, 68, 68, 69]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeFourYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [106, 107, 109, 111, 112, 114, 115]
            intervalMaxPAD = [66, 67, 68, 69, 70, 71, 71]

        if genere == genereGirl:
            intervalMaxPAS = [105, 106, 107, 108, 110, 111, 112]
            intervalMaxPAD = [68, 68, 69, 70, 71, 71, 72]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeFiveYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [108, 109, 110, 112, 114, 115, 116]
            intervalMaxPAD = [69, 70, 71, 72, 73, 74, 74]

        if genere == genereGirl:
            intervalMaxPAS = [107, 107, 108, 110, 111, 112, 113]
            intervalMaxPAD = [70, 71, 71, 72, 73, 73, 74]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeSixYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [109, 110, 112, 114, 115, 117, 117]
            intervalMaxPAD = [72, 72, 73, 74, 75, 76, 76]

        if genere == genereGirl:
            intervalMaxPAS = [108, 109, 110, 111, 113, 114, 115]
            intervalMaxPAD = [72, 72, 73, 74, 74, 75, 76]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeSevenYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [110, 111, 113, 115, 117, 118, 119]
            intervalMaxPAD = [74, 74, 75, 76, 77, 78, 78]

        if genere == genereGirl:
            intervalMaxPAS = [110, 111, 112, 113, 115, 116, 116]
            intervalMaxPAD = [73, 74, 74, 75, 76, 76, 77]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeEightYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [111, 112, 114, 116, 118, 119, 120]
            intervalMaxPAD = [75, 76, 77, 78, 79, 79, 80]

        if genere == genereGirl:
            intervalMaxPAS = [112, 112, 114, 115, 116, 118, 118]
            intervalMaxPAD = [75, 75, 75, 76, 77, 78, 78]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeNineYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [113, 114, 116, 118, 119, 121, 121]
            intervalMaxPAD = [76, 77, 78, 79, 80, 81, 81]

        if genere == genereGirl:
            intervalMaxPAS = [114, 114, 115, 117, 118, 119, 120]
            intervalMaxPAD = [76, 76, 76, 77, 78, 79, 79]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeTenYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [115, 116, 117, 119, 121, 122, 123]
            intervalMaxPAD = [77, 78, 79, 80, 81, 81, 82]

        if genere == genereGirl:
            intervalMaxPAS = [116, 116, 117, 119, 120, 121, 122]
            intervalMaxPAD = [77, 77, 77, 78, 79, 80, 80]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeElevenYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [117, 118, 119, 121, 123, 124, 125]
            intervalMaxPAD = [78, 78, 79, 80, 81, 82, 82]

        if genere == genereGirl:
            intervalMaxPAS = [118, 118, 119, 121, 122, 123, 124]
            intervalMaxPAD = [78, 78, 78, 79, 80, 81, 81]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeTwelveYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [119, 120, 122, 123, 125, 127, 127]
            intervalMaxPAD = [78, 79, 80, 81, 82, 82, 83]

        if genere == genereGirl:
            intervalMaxPAS = [119, 120, 121, 123, 124, 125, 126]
            intervalMaxPAD = [79, 79, 79, 80, 81, 82, 82]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeThirteenYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [121, 122, 124, 126, 128, 129, 130]
            intervalMaxPAD = [79, 79, 80, 81, 82, 83, 83]

        if genere == genereGirl:
            intervalMaxPAS = [121, 122, 123, 124, 126, 127, 128]
            intervalMaxPAD = [80, 80, 80, 81, 82, 83, 83]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeFourteenYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [124, 125, 127, 128, 130, 132, 132]
            intervalMaxPAD = [80, 80, 81, 82, 83, 84, 84]

        if genere == genereGirl:
            intervalMaxPAS = [123, 123, 125, 126, 127, 129, 129]
            intervalMaxPAD = [81, 81, 81, 82, 83, 84, 84]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeFifteenYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [126, 127, 129, 131, 133, 134, 135]
            intervalMaxPAD = [81, 81, 82, 83, 84, 85, 85]

        if genere == genereGirl:
            intervalMaxPAS = [124, 125, 126, 127, 129, 130, 131]
            intervalMaxPAD = [82, 82, 82, 83, 84, 85, 85]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeSixteenYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [129, 130, 132, 134, 135, 137, 137]
            intervalMaxPAD = [82, 83, 83, 84, 85, 86, 87]

        if genere == genereGirl:
            intervalMaxPAS = [125, 126, 127, 128, 130, 131, 132]
            intervalMaxPAD = [82, 82, 83, 84, 85, 85, 86]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeSeventeenYear(self, genere):
        intervalMaxPAS = None
        intervalMaxPAD = None

        if genere == genereBoy:
            intervalMaxPAS = [131, 132, 134, 136, 138, 139, 140]
            intervalMaxPAD = [84, 85, 86, 87, 87, 88, 89]

        if genere == genereGirl:
            intervalMaxPAS = [125, 126, 127, 129, 130, 131, 132]
            intervalMaxPAD = [82, 83, 83, 84, 85, 85, 86]

        result = classifyPPA(self.value, intervalMaxPAS, intervalMaxPAD)
        return result

    def ppaCalculeEighteenYear(self):
        result = normal

        if self.value[indexValuePPA] > 120 or self.value[indexValuePPD] > 80:
            result = hypertension

        return result
