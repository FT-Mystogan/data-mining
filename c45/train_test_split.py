import os
import random

from read_data import get_data, get_names


def train_test_split(dataset_name, data_path, names_path, save_folder, ratio):
    new_training_path = save_folder + '/' + str(ratio) + '/training/' + dataset_name
    new_testing_path = save_folder + '/' + str(ratio) + '/testing/' + dataset_name
    data = get_data(data_path)
    attributes, attr_values, classes = get_names(names_path)
    split_point = round(len(data) * ratio) - 1
    training_data = []
    testing_data = []
    random.shuffle(data)
    for idx, row in enumerate(data):
        if idx <= split_point:
            training_data.append(row)
        else:
            testing_data.append(row)
    write_file(new_training_path + '.data', training_data)
    write_file(new_testing_path + '.data', testing_data)
    write_arff_file(new_training_path + str(ratio) + '.arff', dataset_name, attributes,
                    attr_values, classes, training_data)
    write_arff_file(new_testing_path + str(ratio) + '.arff', dataset_name, attributes,
                    attr_values, classes, testing_data)
    return training_data, testing_data


def write_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w+") as new_file:
        for row in data:
            # row.append(row.pop(0))  # move classification to the last position
            for idx, value in enumerate(row):
                if idx == len(row) - 1:
                    new_file.write(value + "\n")
                else:
                    new_file.write(value + ",")


def write_arff_file(path, dataset_name, attrs, attr_values, classes, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w+") as new_file:
        new_file.write('@RELATION ' + dataset_name + '\n \n')
        for a in attrs:
            if attr_values[a][0] == 'continuous':
                new_file.write('@ATTRIBUTE ' + a + ' numeric \n')
            else:
                new_file.write('@ATTRIBUTE ' + a + ' {')
                for idx, v in enumerate(attr_values[a]):
                    if idx == len(attr_values[a]) - 1:
                        new_file.write(v + "}\n")
                    else:
                        new_file.write(v + ",")

        new_file.write('@ATTRIBUTE class {')
        for idx, c in enumerate(classes):
            if idx == len(classes) - 1:
                new_file.write(c + "}\n\n")
            else:
                new_file.write(c + ",")

        new_file.write('@DATA \n')
        for row in data:
            # row.append(row.pop(0))  # move classification to the last position
            for idx, value in enumerate(row):
                if idx == len(row) - 1:
                    new_file.write(value + "\n")
                else:
                    new_file.write(value + ",")


# ratio: tỉ lệ chia data

# train_test_split('car', 'data/car/1.0/car.data', 'data/car/1.0/car.c45-names', 'data/car', 0.8)
train_test_split('ecoli', 'data/ecoli/1.0/ecoli.data', 'data/ecoli/1.0/ecoli.names', 'data/ecoli', 1.0)
