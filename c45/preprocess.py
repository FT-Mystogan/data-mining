def preprocess():
    data = []
    with open('data/breast-cancer/breast-cancer.data', "r") as file:
        for line in file:
            row = [x.strip() for x in line.split(",")]
            data.append(row)
    with open('data/breast-cancer/breast-cancer-new.data', "w") as newFile:
        for row in data:
            row.append(row.pop(0)) # move classification to the last position
            for idx in range(len(row)-1):
                newFile.write(str(row[idx]) + ",")
            newFile.write(str(row[len(row)-1]) + "\n")

preprocess()