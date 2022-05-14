import math


# logarith co so 2
def log(x):
    if x == 0:
        return 0
    else:
        return math.log(x, 2)


def entropy(data, classes):
    data_len = len(data)
    if data_len == 0:
        return 0
    num_classes = [0 for i in classes]
    # dem so class xuat hien trong dataset
    for row in data:
        class_idx = list(classes).index(row[-1])
        num_classes[class_idx] += 1
    # chia S ra tan so xuat hien cua lop do trong data hien tai
    num_classes = [x / data_len for x in num_classes]
    ent = 0
    # tinh entropy
    for num in num_classes:
        ent += num * log(num)
    return -ent


def split_info(subsets, total_set):
    split_info = 0
    for subset in subsets:
        split_info += - (len(subset) / total_set) * log(len(subset) / total_set)
    return split_info


# do tang thong tin khi chia thanh cac tap con
def gain_ratio(unionSet, subsets, classes):  # gain split
    # input : data and disjoint subsets of it
    # output : information gain
    S = len(unionSet)
    # calculate impurity before split
    impurityBeforeSplit = entropy(unionSet,classes)  # parent node entropy
    # calculate impurity after split
    weights = [len(subset) / S for subset in subsets]
    impurityAfterSplit = 0  # child nodes entropy
    for i in range(len(subsets)):
        impurityAfterSplit += weights[i] * entropy(subsets[i], classes)
    # calculate total gain
    totalGain = impurityBeforeSplit - impurityAfterSplit
    # split info
    splitInfo = split_info(subsets, S)
    if totalGain == 0:
        return 0
    ratio = totalGain / splitInfo
    return ratio

# def gain(unionSet, subsets, classes):
#     S = len(unionSet)
#     impurityBeforeSplit = entropy(unionSet, classes)  # parent node entropy
#     weights = [len(subset) / S for subset in subsets]
#     impurityAfterSplit = 0  # child nodes entropy
#     for i in range(len(subsets)):
#         impurityAfterSplit += weights[i] * entropy(subsets[i], classes)
#     # calculate total gain
#     totalGain = impurityBeforeSplit - impurityAfterSplit
#
#     if totalGain == 0:
#         return 0
#     return totalGain