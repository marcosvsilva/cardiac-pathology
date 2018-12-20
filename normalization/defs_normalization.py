from unicodedata import normalize
from dateutil import parser
from defs_normalization_ppa import DefsNormalizationPPA

# Atributes DataSet
attributes = {'ID': 0, 'PESO': 1, 'ALTURA': 2, 'IMC': 3, 'ATENDIMENTO': 4, 'ANIVERSARIO': 5, 'IDADE': 6,
              'CONVERNIO': 7, 'PULSO': 8, 'PASISTOLICA': 9, 'PADIASTOLICA': 10, 'PPA': 11, 'NORMALXANORMAL': 12,
              'B2': 13, 'SOPRO': 14, 'FC': 15, 'HDA1': 16, 'HDA2': 17, 'SEXO': 18, 'REASON1': 19, 'REASON2': 20}

convert_height_to_cm = 100

missing_value = ''


def calculate_age(attendance, birthday):
    try:
        age = attendance.year - birthday.year
        month = attendance.month - birthday.month
        date = attendance.day - birthday.day

        age = int(age)
        month = int(month)
        date = int(date)

        if month < 0:
            age = age - 1
        elif date < 0 and month == 0:
            age = age - 1
    except ValueError:
        age = -1

    return age


def check_imc(imc, max_value, min_value):
    try:
        imc = float(imc)
        max_value = float(max_value)
        min_value = float(min_value)

        if min_value <= imc <= max_value:
            imc = round(imc, 2)
        else:
            imc = -1

    except ValueError:
        imc = -1

    return imc


def check_ppa(ppa):
    ppa_new = missing_value
    if ppa != '':
        if ppa in ['NORMAL']:
            ppa_new = 'NORMAL'

        if ppa in ['PRE-HIPERTENSAO PAS', 'PRE-HIPERTENSAO PAD', 'HAS-1 PAS', 'HAS-1 PAD', 'HAS-3 PAS', 'HAS-3 PAD']:
            ppa_new = 'HAS'

    return ppa_new


def replace_invalid_interest_arguments_recursive(line):
    if '#VALUE!' in line:
        index = line.index('#VALUE!')
        line[index] = missing_value
        replace_invalid_interest_arguments_recursive(line)

    if ',' in line:
        index = line.index(',')
        line[index] = '.'
        replace_invalid_interest_arguments_recursive(line)

    return line


def move_last_position_class_recursive(line, position):
    if position == line.__len__() - 1:
        return line
    else:
        aux = line[position]
        line[position] = line[position + 1]
        line[position + 1] = aux
        return move_last_position_class_recursive(line, position + 1)


class AttributesDataset:
    def get_attributes_dataset():
        return attributes


class AttributesClass:
    def get_index_attribute_class(line, attribute):
        index = -1
        for i in range(len(line)):
            if line[i] == attribute:
                index = i
                break
        return index


class DefsNormalization:
    # values for processing
    max_value_fc = 0
    min_value_fc = 0

    max_value_pa = 0
    min_value_pa = 0

    max_value_imc = 0
    min_value_imc = 0

    max_value_age = 0
    min_value_age = 0

    max_value_weight = 0
    min_value_weight = 0

    max_value_height = 0
    min_value_height = 0

    attributes_remove = []
    missing_values_genere = False
    max_value_conversion_height = 0
    remove_attribute_age_out_range = False

    # class of normalization PPA
    normalization_ppa = None

    def __init__(self, max_value_fc, min_value_fc, max_value_pa, min_value_pa, max_value_imc, min_value_imc,
                 max_value_age, min_value_age, max_value_weight, min_value_weight, max_value_height, min_value_height,
                 attributes_remove, missing_values_genere, max_value_conversion_height, remove_attribute_age_out_range):
        self.max_value_fc = max_value_fc
        self.min_value_fc = min_value_fc

        self.max_value_pa = max_value_pa
        self.min_value_pa = min_value_pa

        self.max_value_imc = max_value_imc
        self.min_value_imc = min_value_imc

        self.max_value_age = max_value_age
        self.min_value_age = min_value_age

        self.max_value_weight = max_value_weight
        self.min_value_weight = min_value_weight

        self.max_value_height = max_value_height
        self.min_value_height = min_value_height

        self.attributes_remove = attributes_remove
        self.missing_values_genere = missing_values_genere
        self.max_value_conversion_height = max_value_conversion_height
        self.remove_attribute_age_out_range = remove_attribute_age_out_range

        # class of normalization PPA
        self.normalization_ppa = DefsNormalizationPPA(min_value_pa, min_value_pa)

    def remove_expendable_attribute(self, line):
        for index in self.attributes_remove:
            line.pop(index)
        return line

    def replace_invalid_interest_arguments(self, line):
        return replace_invalid_interest_arguments_recursive(line)

    def move_last_position_class(self, line, index):
        return move_last_position_class_recursive(line, index)

    def process_normal_anormal(self, line):
        if line[attributes['NORMALXANORMAL']] != 'NORMAL X ANORMAL':
            if line[attributes['NORMALXANORMAL']] in ('NORMAL', 'NORMAIS'):
                line[attributes['NORMALXANORMAL']] = 'NORMAL'

            elif line[attributes['NORMALXANORMAL']] in ('ANORMAL'):
                line[attributes['NORMALXANORMAL']] = 'ANORMAL'

            else:
                line[attributes['NORMALXANORMAL']] = missing_value

        return line

    def replace_accentuation_upper(self, line):
        for i in range(len(line)):
            line[i] = normalize('NFKD', line[i]).encode('ASCII', 'ignore').decode('ASCII')
            line[i] = line[i].upper()

        return line

    def process_sexo(self, line):
        if line[attributes['SEXO']] != 'SEXO':
            if line[attributes['SEXO']] in ('M', 'MASCULINO'):
                line[attributes['SEXO']] = 'MASCULINO'

            elif line[attributes['SEXO']] in ('F', 'FEMININO'):
                line[attributes['SEXO']] = 'FEMININO'

            elif line[attributes['SEXO']] in ('INDETERMINADO'):
                if self.missing_values_genere:
                    line[attributes['SEXO']] = missing_value
                else:
                    line[attributes['SEXO']] = 'INDETERMINADO'

        return line

    def process_idade(self, line):
        if line[attributes['IDADE']] != 'IDADE':
            try:
                attendance = parser.parse(line[attributes['ATENDIMENTO']])
            except ValueError:
                attendance = None

            try:
                birthday = parser.parse(line[attributes['ANIVERSARIO']])
            except ValueError:
                birthday = None

            if (attendance is not None) and (birthday is not None):
                age = calculate_age(attendance, birthday)

                if self.min_value_age <= age <= self.max_value_age:
                    line[attributes['IDADE']] = age
                else:
                    line[attributes['IDADE']] = missing_value
            else:
                line[attributes['IDADE']] = missing_value

        return line

    def process_pas(self, line):
        if line[attributes['PASISTOLICA']] != 'PA SISTOLICA':
            pas = -1

            if line[attributes['PASISTOLICA']] != missing_value:
                pas = int(line[attributes['PASISTOLICA']])

            if self.min_value_pa <= pas < self.max_value_pa:
                line[attributes['PASISTOLICA']] = pas
            else:
                line[attributes['PASISTOLICA']] = missing_value

        return line

    def process_pad(self, line):
        if line[attributes['PADIASTOLICA']] != 'PA DIASTOLICA':
            pad = -1

            if line[attributes['PADIASTOLICA']] != missing_value:
                pad = int(line[attributes['PADIASTOLICA']])

            if self.min_value_pa <= pad < self.max_value_pa:
                line[attributes['PADIASTOLICA']] = pad
            else:
                line[attributes['PADIASTOLICA']] = missing_value

        return line

    def process_ppa(self, line):
        if line[attributes['PPA']] != 'PPA':
            line = self.process_pas(line)
            line = self.process_pad(line)

            genere = missing_value
            if line[attributes['SEXO']] != missing_value:
                genere = line[attributes['SEXO']]

            age = 0
            if line[attributes['IDADE']] != missing_value:
                age = int(line[attributes['IDADE']])

            height = 0
            if line[attributes['ALTURA']] != missing_value:
                height = int(line[attributes['ALTURA']])

            pas = 0
            if line[attributes['PASISTOLICA']] != missing_value:
                pas = int(line[attributes['PASISTOLICA']])

            pad = 0
            if line[attributes['PADIASTOLICA']] != missing_value:
                pad = int(line[attributes['PADIASTOLICA']])

            result = self.normalization_ppa.ppa_calculate(genere, age, height, pas, pad)

            if result == missing_value:
                result = check_ppa(line[attributes['PPA']])

            line[attributes['PPA']] = result
        return line

    def process_peso(self, line):
        if line[attributes['PESO']] != 'PESO':
            if line[attributes['PESO']] != missing_value:
                try:
                    weight = float(line[attributes['PESO']])

                    if self.min_value_height <= weight <= self.max_value_weight:
                        line[attributes['PESO']] = weight
                    else:
                        line[attributes['PESO']] = missing_value

                except ValueError:
                    line[attributes['PESO']] = missing_value

        return line

    def process_altura(self, line):
        if line[attributes['ALTURA']] != 'ALTURA':
            try:
                if line[attributes['ALTURA']] != '':
                    height_aux = int(line[attributes['ALTURA']])

                    if self.min_value_height <= height_aux <= self.max_value_height:
                        height = height_aux
                        line[attributes['ALTURA']] = height
                    else:
                        line[attributes['ALTURA']] = missing_value

            except ValueError:
                line[attributes['ALTURA']] = missing_value

        return line

    def process_imc(self, line):
        if line[attributes['IMC']] != 'IMC':
            try:
                line = self.process_altura(line)
                height = float(line[attributes['ALTURA']])
            except ValueError:
                height = 0

            try:
                line = self.process_peso(line)
                weight = float(line[attributes['PESO']])
            except ValueError:
                weight = 0

            if (height > 0) and (weight > 0):
                if height > self.max_value_conversion_height:
                    height = height / convert_height_to_cm

                imc = weight / (height * height)
                imc = check_imc(imc, self.max_value_imc, self.min_value_imc)

                if imc > 0:
                    line[attributes['IMC']] = imc
                else:
                    line[attributes['IMC']] = missing_value

            elif line[attributes['IMC']] != missing_value:
                imc = check_imc(line[attributes['IMC']], self.max_value_imc, self.min_value_imc)

                if imc > 0:
                    line[attributes['IMC']] = imc
                else:
                    line[attributes['IMC']] = missing_value

        return line

    def process_fc(self, line):
        if line[attributes['FC']] != 'FC':
            if line[attributes['FC']] != '':
                try:
                    int_fc = int(line[attributes['FC']])

                    if self.min_value_fc <= int_fc <= self.max_value_fc:
                        line[attributes['FC']] = int_fc
                    else:
                        line[attributes['FC']] = missing_value

                except ValueError:
                    line[attributes['FC']] = missing_value

        return line

    def merge_motivos(self, line, index_attribute_motivo1, index_attribute_motivo2):
        if (index_attribute_motivo1 > -1) and (index_attribute_motivo2 > -1):
            reason1 = str(line[index_attribute_motivo1])
            reason2 = str(line[index_attribute_motivo2])

            if reason1 != missing_value and reason2 != missing_value:
                if reason1 == 'MOTIVO1':
                    line[index_attribute_motivo1] = 'MOTIVO'
                else:
                    if reason2 != missing_value:
                        line[index_attribute_motivo1] = reason2

                    if line[index_attribute_motivo1] in ['07 - OUTRO']:
                        line[index_attribute_motivo1] = 'OUTRO'

        line.pop(index_attribute_motivo2)
        return line

    def valid_age(self, line):
        result = True
        if self.remove_attribute_age_out_range:
            if line[attributes['IDADE']] != 'IDADE':
                result = not (line[attributes['IDADE']] == missing_value)
        return result

    def discretize_atribute(self, line, index, interval):
        try:
            if index >= 0:
                if line[index] != '':
                    value = float(line[index])

                    for values_interval in interval:
                        min_value = float(values_interval[0])
                        max_value = float(values_interval[1])

                        if min_value <= value < max_value:
                            line[index] = 'Class[' + str(values_interval[0]) + ',' + str(values_interval[1]) + ')'

            return line
        except ValueError:
            line = 'FAIL OF DISCRETIZE INDEX ' + str(index)
