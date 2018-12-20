import csv
import os
from defs_normalization import DefsNormalization, AttributesDataset, AttributesClass

# Moldable Parameters for Data Normalization
# Max and min values for attributes
max_value_fc = 250
min_value_fc = 40

max_value_pa = 250
min_value_pa = 40

max_value_imc = 60.0
min_value_imc = 1.0

max_value_age = 18
min_value_age = 0

max_value_weight = 500.0
min_value_weight = 0.1

max_value_height = 350
min_value_height = 1

# Max and min values for discretize (group-by)
class_discretize_peso = [[0, 35], [35, 70], [70, 105], [105, 140], [140, 175]]
class_discretize_altura = [[0, 40], [40, 80], [80, 120], [120, 160], [160, 200]]
class_discretize_imc = [[0, 12], [12, 24], [24, 36], [36, 48], [48, 60]]
class_discretize_idade = [[0, 4], [4, 8], [8, 12], [12, 16], [16, 20]]
class_discretize_pas = [[0, 50], [50, 100], [100, 150], [150, 200], [200, 250]]
class_discretize_pad = [[0, 50], [50, 100], [100, 150], [150, 200], [200, 250]]
class_discretize_fc = [[0, 50], [50, 100], [100, 150], [150, 200], [200, 250]]

# Remove attributes unnecessary from dataset
attributes_remove = []

# Replaces the UNDEFINED genders with missing values
missing_values_genere = True

# Maximum value to express height in meters, so that no conversion is required
max_value_to_conversion_height = 4

# Removes any record that has the age outside the minimum and maximum range
remove_attribute_age_out_range = True

# Directory containing the original dataset in csv UTF-8
dataset_csv_directory = '../DataSet/'

# Original dataset in csv UTF-8
dataset_csv_input = dataset_csv_directory + 'dataset_original.csv'

# Normalized dataset output
dataset_csv_output = dataset_csv_directory + 'dataset_normalization.csv'

# Removes output dataset before execution
if os.path.isfile(dataset_csv_output):
    os.remove(dataset_csv_output)

# Document content CSV original processed
processed_document = []
normalize_document = []

# Class of index fields
attributes_dataset = AttributesDataset
attributes_class = AttributesClass

# Remove attributes unnecessary from dataset
attributes_dataset = attributes_dataset.get_attributes_dataset()

# Attributes to be removed
attributes_remove.append(attributes_dataset['HDA2'])
attributes_remove.append(attributes_dataset['PPA'])
attributes_remove.append(attributes_dataset['CONVERNIO'])
attributes_remove.append(attributes_dataset['ANIVERSARIO'])
attributes_remove.append(attributes_dataset['ATENDIMENTO'])
attributes_remove.append(attributes_dataset['ID'])

# Read Original DataSet exections functions normalization write DataSet Ouput
normalization = DefsNormalization(max_value_fc, min_value_fc, max_value_pa, min_value_pa, max_value_imc, min_value_imc,
                                  max_value_age, min_value_age, max_value_weight, min_value_weight, max_value_height,
                                  min_value_height, attributes_remove, missing_values_genere,
                                  max_value_to_conversion_height, remove_attribute_age_out_range)

# Read and processed original document
first_line = True
index_interest_class = 0
with open(dataset_csv_input, newline='', encoding='utf-8') as reader_csv:
    reader = csv.reader(reader_csv)

    for row in reader:
        if row[attributes_dataset['NORMALXANORMAL']] != '':
            line = normalization.replace_invalid_interest_arguments(row)
            line = normalization.replace_accentuation_upper(line)

            if not first_line:
                line = normalization.process_normal_anormal(line)
                line = normalization.process_idade(line)
                line = normalization.process_sexo(line)
                line = normalization.process_altura(line)
                line = normalization.process_peso(line)
                line = normalization.process_imc(line)
                line = normalization.process_fc(line)
                line = normalization.process_pas(line)
                line = normalization.process_pad(line)
                line = normalization.process_ppa(line)

            if normalization.valid_age(line):
                line = normalization.remove_expendable_attribute(line)

                if first_line:
                    index_interest_class = attributes_class.get_index_attribute_class(line, 'NORMAL X ANORMAL')
                    first_line = False

                line = normalization.move_last_position_class(line, index_interest_class)
                processed_document.append(line)

#  Discretize, and merge attributes
first_line = True
index_class_peso = -1
index_class_altura = -1
index_class_imc = -1
index_class_idade = -1
index_class_pas = -1
index_class_pad = -1
index_class_fc = -1
index_class_motivo1 = -1
index_class_motivo2 = -1


with open(dataset_csv_output, 'w', newline='', encoding='utf-8') as csvWriterFile:
    writerCSV = csv.writer(csvWriterFile)

    for line in processed_document:
        if first_line:
            index_class_peso = attributes_class.get_index_attribute_class(line, 'PESO')
            index_class_altura = attributes_class.get_index_attribute_class(line, 'ALTURA')
            index_class_imc = attributes_class.get_index_attribute_class(line, 'IMC')
            index_class_idade = attributes_class.get_index_attribute_class(line, 'IDADE')
            index_class_pas = attributes_class.get_index_attribute_class(line, 'PA SISTOLICA')
            index_class_pad = attributes_class.get_index_attribute_class(line, 'PA DIASTOLICA')
            index_class_fc = attributes_class.get_index_attribute_class(line, 'FC')
            index_class_motivo1 = attributes_class.get_index_attribute_class(line, 'MOTIVO1')
            index_class_motivo2 = attributes_class.get_index_attribute_class(line, 'MOTIVO2')

            line = normalization.merge_motivos(line, index_class_motivo1, index_class_motivo2)  # remove title MOTIVO2

            first_line = False
        else:
            line = normalization.discretize_atribute(line, index_class_peso, class_discretize_peso)
            line = normalization.discretize_atribute(line, index_class_altura, class_discretize_altura)
            line = normalization.discretize_atribute(line, index_class_imc, class_discretize_imc)
            line = normalization.discretize_atribute(line, index_class_idade, class_discretize_idade)
            line = normalization.discretize_atribute(line, index_class_pas, class_discretize_pas)
            line = normalization.discretize_atribute(line, index_class_pad, class_discretize_pad)
            line = normalization.discretize_atribute(line, index_class_fc, class_discretize_fc)

            line = normalization.merge_motivos(line, index_class_motivo1, index_class_motivo2)

        writerCSV.writerow(line)