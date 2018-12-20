# Classification of PPA
normal = 'NORMAL'
hypertension = 'HAS'
missing_value = ''

genere_boy = 'MASCULINO'
genere_girl = 'FEMININO'

index_value_height = 'HEIGHT'
index_value_ppa = 'PPA'
index_value_ppd = 'PPD'

interval_percentil = [[0, 5], [5, 10], [10, 25], [25, 50], [50, 75], [75, 90]]


def create_value(height, value_min_ppa, value_min_ppd, value_ppa, value_ppd):
    value = None

    if height > 0 and value_ppa > value_min_ppa and value_ppd > value_min_ppd:
        value = {index_value_height: height, index_value_ppa: value_ppa, index_value_ppd: value_ppd}

    return value


def classify(value, max_pas, max_pad):
    result = missing_value

    if value[index_value_ppa] >= max_pas or value[index_value_ppd] >= max_pad:
        result = hypertension
    else:
        result = normal

    return result


def classify_ppa(value, interval_max_pas, interval_max_pad):
    result = missing_value
    index = -1
    count = 0
    max = 0

    for interval in interval_percentil:
        min = interval[0]
        max = interval[1]

        if min < value[index_value_height] <= max:
            index = count

        count += 1

    if value[index_value_height] > max:
        index = count

    if index >= 0:
        result = classify(value, interval_max_pas[index], interval_max_pad[index])

    return result


class DefsNormalizationPPA:
    value = None
    value_min_ppa = 0
    value_min_ppd = 0

    def __init__(self, value_min_ppa, value_min_ppd):
        self.value_min_ppa = value_min_ppa
        self.value_min_ppd = value_min_ppd

    def ppa_calculate(self, genere, age, height, pas, pad):
        result = missing_value

        if genere != missing_value:
            value = create_value(height, self.value_min_ppd, self.value_min_ppa, pas, pad)

            if value is not None:
                self.value = value
                result = self.ppa_calculate_list(age, genere)

        return result

    def ppa_calculate_list(self, age, genere):
        result = missing_value

        if age in [0, 1]:
            result = self.ppa_calcule_one_year(genere)
        elif age == 2:
            result = self.ppa_calcule_two_year(genere)
        elif age == 3:
            result = self.ppa_calcule_three_year(genere)
        elif age == 4:
            result = self.ppa_calcule_four_year(genere)
        elif age == 5:
            result = self.ppa_calcule_five_year(genere)
        elif age == 6:
            result = self.ppa_calcule_six_year(genere)
        elif age == 7:
            result = self.ppa_calcule_seven_year(genere)
        elif age == 8:
            result = self.ppa_calcule_eight_year(genere)
        elif age == 9:
            result = self.ppa_calcule_nine_year(genere)
        elif age == 10:
            result = self.ppa_calcule_ten_year(genere)
        elif age == 11:
            result = self.ppa_calcule_eleven_year(genere)
        elif age == 12:
            result = self.ppa_calcule_twelve_year(genere)
        elif age == 13:
            result = self.ppa_calcule_thirteen_year(genere)
        elif age == 14:
            result = self.ppa_calcule_fourteen_year(genere)
        elif age == 15:
            result = self.ppa_calcule_fifteen_year(genere)
        elif age == 16:
            result = self.ppa_calcule_sixteen_year(genere)
        elif age == 17:
            result = self.ppa_calcule_seventeen_year(genere)
        else:
            result = self.ppa_calcule_eighteen_year()

        return result

    #  Classification
    def ppa_calcule_one_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [98, 99, 101, 103, 104, 106, 106]
            interval_max_pad = [54, 54, 55, 56, 57, 58, 58]

        if genere == genere_girl:
            interval_max_pas = [100, 101, 102, 104, 105, 106, 107]
            interval_max_pad = [56, 57, 57, 58, 59, 59, 60]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_two_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [101, 102, 104, 106, 108, 109, 110]
            interval_max_pad = [59, 59, 60, 61, 62, 63, 63]

        if genere == genere_girl:
            interval_max_pas = [102, 103, 104, 105, 107, 108, 109]
            interval_max_pad = [61, 62, 62, 63, 64, 65, 65]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_three_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [104, 105, 107, 109, 110, 112, 113]
            interval_max_pad = [63, 63, 64, 65, 66, 67, 67]

        if genere == genere_girl:
            interval_max_pas = [104, 104, 105, 107, 108, 109, 110]
            interval_max_pad = [65, 66, 66, 67, 68, 68, 69]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_four_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [106, 107, 109, 111, 112, 114, 115]
            interval_max_pad = [66, 67, 68, 69, 70, 71, 71]

        if genere == genere_girl:
            interval_max_pas = [105, 106, 107, 108, 110, 111, 112]
            interval_max_pad = [68, 68, 69, 70, 71, 71, 72]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_five_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [108, 109, 110, 112, 114, 115, 116]
            interval_max_pad = [69, 70, 71, 72, 73, 74, 74]

        if genere == genere_girl:
            interval_max_pas = [107, 107, 108, 110, 111, 112, 113]
            interval_max_pad = [70, 71, 71, 72, 73, 73, 74]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_six_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [109, 110, 112, 114, 115, 117, 117]
            interval_max_pad = [72, 72, 73, 74, 75, 76, 76]

        if genere == genere_girl:
            interval_max_pas = [108, 109, 110, 111, 113, 114, 115]
            interval_max_pad = [72, 72, 73, 74, 74, 75, 76]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_seven_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [110, 111, 113, 115, 117, 118, 119]
            interval_max_pad = [74, 74, 75, 76, 77, 78, 78]

        if genere == genere_girl:
            interval_max_pas = [110, 111, 112, 113, 115, 116, 116]
            interval_max_pad = [73, 74, 74, 75, 76, 76, 77]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_eight_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [111, 112, 114, 116, 118, 119, 120]
            interval_max_pad = [75, 76, 77, 78, 79, 79, 80]

        if genere == genere_girl:
            interval_max_pas = [112, 112, 114, 115, 116, 118, 118]
            interval_max_pad = [75, 75, 75, 76, 77, 78, 78]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_nine_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [113, 114, 116, 118, 119, 121, 121]
            interval_max_pad = [76, 77, 78, 79, 80, 81, 81]

        if genere == genere_girl:
            interval_max_pas = [114, 114, 115, 117, 118, 119, 120]
            interval_max_pad = [76, 76, 76, 77, 78, 79, 79]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_ten_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [115, 116, 117, 119, 121, 122, 123]
            interval_max_pad = [77, 78, 79, 80, 81, 81, 82]

        if genere == genere_girl:
            interval_max_pas = [116, 116, 117, 119, 120, 121, 122]
            interval_max_pad = [77, 77, 77, 78, 79, 80, 80]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_eleven_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [117, 118, 119, 121, 123, 124, 125]
            interval_max_pad = [78, 78, 79, 80, 81, 82, 82]

        if genere == genere_girl:
            interval_max_pas = [118, 118, 119, 121, 122, 123, 124]
            interval_max_pad = [78, 78, 78, 79, 80, 81, 81]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_twelve_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [119, 120, 122, 123, 125, 127, 127]
            interval_max_pad = [78, 79, 80, 81, 82, 82, 83]

        if genere == genere_girl:
            interval_max_pas = [119, 120, 121, 123, 124, 125, 126]
            interval_max_pad = [79, 79, 79, 80, 81, 82, 82]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_thirteen_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [121, 122, 124, 126, 128, 129, 130]
            interval_max_pad = [79, 79, 80, 81, 82, 83, 83]

        if genere == genere_girl:
            interval_max_pas = [121, 122, 123, 124, 126, 127, 128]
            interval_max_pad = [80, 80, 80, 81, 82, 83, 83]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_fourteen_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [124, 125, 127, 128, 130, 132, 132]
            interval_max_pad = [80, 80, 81, 82, 83, 84, 84]

        if genere == genere_girl:
            interval_max_pas = [123, 123, 125, 126, 127, 129, 129]
            interval_max_pad = [81, 81, 81, 82, 83, 84, 84]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_fifteen_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [126, 127, 129, 131, 133, 134, 135]
            interval_max_pad = [81, 81, 82, 83, 84, 85, 85]

        if genere == genere_girl:
            interval_max_pas = [124, 125, 126, 127, 129, 130, 131]
            interval_max_pad = [82, 82, 82, 83, 84, 85, 85]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_sixteen_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [129, 130, 132, 134, 135, 137, 137]
            interval_max_pad = [82, 83, 83, 84, 85, 86, 87]

        if genere == genere_girl:
            interval_max_pas = [125, 126, 127, 128, 130, 131, 132]
            interval_max_pad = [82, 82, 83, 84, 85, 85, 86]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_seventeen_year(self, genere):
        interval_max_pas = None
        interval_max_pad = None

        if genere == genere_boy:
            interval_max_pas = [131, 132, 134, 136, 138, 139, 140]
            interval_max_pad = [84, 85, 86, 87, 87, 88, 89]

        if genere == genere_girl:
            interval_max_pas = [125, 126, 127, 129, 130, 131, 132]
            interval_max_pad = [82, 83, 83, 84, 85, 85, 86]

        result = classify_ppa(self.value, interval_max_pas, interval_max_pad)
        return result

    def ppa_calcule_eighteen_year(self):
        result = normal

        if self.value[index_value_ppa] > 120 or self.value[index_value_ppd] > 80:
            result = hypertension

        return result
