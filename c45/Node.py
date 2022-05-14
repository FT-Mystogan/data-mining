# gom nhan, nguong(neu co), la nut la, cac nut con
class Node:
    _id = 0

    def __init__(self, is_leaf, label, threshold, maj_class, data):
        self._id = Node._id
        Node._id += 1
        self.label = label
        self.threshold = threshold
        self.is_leaf = is_leaf
        self.children = []
        self.maj_class = maj_class  # class xuat hien nhieu nhat trong subset tai node do
        self.subset_data = data