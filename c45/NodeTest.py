class NodeTest:
    def __init__(self, _id, is_leaf, label, children, threshold, maj_class, subset_data):
        self._id = _id
        self.label = label
        self.threshold = threshold
        self.is_leaf = is_leaf
        list_children = []
        for x in children:
            list_children.append(NodeTest(**x))
        self.children = list_children
        self.maj_class = maj_class  # class xuat hien nhieu nhat trong subset tai node do
        self.subset_data = subset_data
