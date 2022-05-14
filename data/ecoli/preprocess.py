def preprocess():
    data = []
    with open('1.0/ecoli.data', "r") as file:
        for line in file:
            row = [x.strip() for x in line.split("  ")]
            data.append(row)
    with open('1.0/ecoli.data', "w+") as new_file:
        for row in data:
            row.pop(0)
            # row.append(row.pop(0)) # move classification to the last position
            for idx in range(len(row)-1):
                new_file.write(str(row[idx]) + ",")
            new_file.write(str(row[len(row)-1]) + "\n")

preprocess()