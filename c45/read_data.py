
def get_data(data_path):
    data = []
    with open(data_path, "r") as file:
        for line in file:
            row = [x.strip() for x in line.split(",")]
            if row != [] or row != [""]:
                data.append(row)
    return data


def get_names(names_path):
    with open(names_path, "r") as file:
        classes = file.readline()
        classes = [x.strip() for x in classes.split(",")]
        attr_values = {}
        for line in file:
            [attribute, values] = [x.strip() for x in line.split(":")]
            values = [x.strip() for x in values.split(",")]
            attr_values[attribute] = values
    attributes = list(attr_values.keys())
    return attributes, attr_values, classes