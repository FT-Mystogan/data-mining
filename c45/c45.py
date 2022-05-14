from Node import Node
from cal_gain_ratio import gain_ratio
from read_data import get_data, get_names


class C45:

    def __init__(self, training_path, testing_path, names_path):
        # Đường dẫn
        self.training_path = training_path
        self.testing_path = testing_path
        self.names_path = names_path

        self.classes = []  # Lớp phân loại
        self.attr_values = {}  # Giá trị các thuộc tính
        self.attributes = []  # Thuộc tính

        self.tree = None  # Cây
        self.pruned_tree = None  # Cây được tỉa

        self.count_leaf = 0
        self.count_node = 0

        self.matrix = {}
        # Dữ liệu
        self.training_data = []
        self.testing_data = []
        self.min_number_of_instances = 2 

    # đọc dữ liệu từ file ra 2 tập train và test
    def get_data(self):
        (self.attributes, self.attr_values, self.classes) = get_names(self.names_path)
        self.training_data = self.pre_process(get_data(self.training_path))
        self.testing_data = self.pre_process(get_data(self.testing_path))

        return self.training_data, self.testing_data

    # tiền xử lý data 
    def pre_process(self, data):
        for idx, row in enumerate(data):
            for attr_idx in range(len(self.attributes)):
                # du lieu lien tuc thi ep kieu string => float
                if self.is_continuous_attr(self.attributes[attr_idx]):
                    data[idx][attr_idx] = float(data[idx][attr_idx])

        return data

    # kiểm tra giá trị có liên tục hay không 
    def is_continuous_attr(self, attribute):
        if len(self.attr_values[attribute]) == 1 and self.attr_values[attribute][0] == "continuous":
            return True
        else:
            return False
    
    # Dự đoán nhãn cuối cùng của cây
    def predict(self, node, data_row):
        if not node.is_leaf:
            # get node attribute index
            node_attr_idx = -1
            for attrIdx in range(len(self.attributes)):
                if self.attributes[attrIdx] == node.label:
                    node_attr_idx = attrIdx
                    break
            if node.threshold is None:
                for idx, child in enumerate(node.children):
                    if data_row[node_attr_idx] == self.attr_values[node.label][idx]:
                        if child.is_leaf:
                            return str(child.label)
                        else:
                            return self.predict(child, data_row)
            else:
                left_child = node.children[0]
                right_child = node.children[1]

                if float(data_row[node_attr_idx]) <= node.threshold:
                    if left_child.is_leaf:
                        return str(left_child.label)
                    else:
                        return self.predict(left_child, data_row)
                else:
                    if right_child.is_leaf:
                        return str(right_child.label)
                    else:
                        return self.predict(right_child, data_row)

    def test(self, tree, data):
        result = []
        error = 0
        correct = 0

        for row in data:
            result.append(self.predict(tree, row))

        for c in self.classes:
            self.matrix[c] = {x: 0 for x in self.classes}
        for idx, r in enumerate(result):
            if data[idx][-1] == r:
                self.matrix[r][r] += 1
                correct += 1
            elif data[idx][-1] != r:
                self.matrix[data[idx][-1]][r] += 1
                error += 1

        for row in self.matrix:
            print(row, end=" ")
            print(self.matrix[row])
        print('accuracy: ' + str(correct / len(data)))

        return error

    def print_tree(self, tree):
        self.count_leaf = 0
        self.count_node = 0
        self.print_node(tree)
        print('number of nodes: ' + str(self.count_node))
        print('number of leaves: ' + str(self.count_leaf))

    def print_node(self, node, indent=""):
        self.count_node += 1
        if not node.is_leaf:
            if node.threshold is None:
                # roi rac
                for index, child in enumerate(node.children):
                    if child.is_leaf:
                        self.count_leaf += 1
                        self.count_node += 1
                        print(indent + node.label + " = " + self.attr_values[node.label][
                            index] + " : " + child.label)
                    else:
                        print(
                            indent + node.label + " = " + self.attr_values[node.label][index])
                        self.print_node(child, indent + "|   ")
            else:
                # lien tuc
                left_child = node.children[0]
                right_child = node.children[1]
                if left_child.is_leaf:
                    self.count_leaf += 1
                    self.count_node += 1
                    print(indent + node.label + " <= " + str(node.threshold) + " : " + left_child.label)
                else:
                    print(indent + node.label + " <= " + str(node.threshold))
                    self.print_node(left_child, indent + "|    ")

                if right_child.is_leaf:
                    self.count_leaf += 1
                    self.count_node += 1
                    print(indent + node.label + " > " + str(node.threshold) + " : " + right_child.label)
                else:
                    print(indent + node.label + " > " + str(node.threshold))
                    self.print_node(right_child, indent + "|   ")

    def generate_tree(self):
        self.tree = self.recursive_generate_tree(self.training_data, self.attributes,
                                               self.get_major_class(self.training_data))

        return self.tree

    def recursive_generate_tree(self, data, cur_attributes, parent_maj_class):

        all_same_class = self.all_same_class(data)
        all_same_attr = self.all_same_attr_value(data, cur_attributes)
        node_maj_class = self.get_major_class(data)
        if len(data) == 0:
            # Fail
            return Node(True, parent_maj_class, None, node_maj_class, None)
        elif all_same_class is not False:
            # return a node with that class
            return Node(True, all_same_class, None, node_maj_class, None)
        elif all_same_attr is True:
            return Node(True, parent_maj_class, None, node_maj_class, None)
        elif len(cur_attributes) == 0:
            # return a node with the majority class
            return Node(True, node_maj_class, None, node_maj_class, None)
        else:
            # chon thuoc tinh, xoa thuoc tinh tot nhat trong danh sach thuoc tinh
            # print(i)
            (best, best_threshold, splitted) = self.split_attribute(data, cur_attributes)

            remaining_attributes = cur_attributes[:]
            remaining_attributes.remove(best)
            node = Node(False, best, best_threshold, node_maj_class, None)

            if best_threshold is None:  # Ap dung cho gia tri roi rac
                count_subset = 0
                for subset in splitted:
                    if len(subset) >= self.min_number_of_instances:
                         count_subset += 1
                if count_subset < 2:
                    return Node(True, parent_maj_class, None, node_maj_class, None)

            node.children = [self.recursive_generate_tree(subset, remaining_attributes, node_maj_class) for subset
                             in splitted]
            node.subset_data = data

            return node

    # Tìm ra class xuất hiện nhiều nhất trong tập dữ liệu
    def get_major_class(self, data):
        freq = [0] * len(self.classes)
        for row in data:
            index = self.classes.index(row[-1])
            freq[index] += 1
        max_idx = freq.index(max(freq))

        return self.classes[max_idx]

    # Kiểm tra xem thuộc tính có cùng giá trị không 
    def all_same_attr_value(self, data, attrs):
        stop = True
        for row in data:
            for a in attrs:
                attr_idx = self.attributes.index(a)
                if data[0][attr_idx] != row[attr_idx]:
                    stop = False
                    return stop

        return stop

    # kiem tra xem du lieu deu chung 1 class khong row[-1] = classname
    def all_same_class(self, data):
        if len(data) == 0:
            return False
        for row in data:
            # so sanh voi class cua data dau tien
            if row[-1] != data[0][-1]:
                return False

        return data[0][-1]

    # Chọn thuộc tính tốt nhất để tạo làm node mới 
    def split_attribute(self, cur_data, cur_attributes):
        splitted = []
        max_ent = 0  # * float("inf")  # -INF entropy luon + ?
        best_attribute = -1
        # None for discrete attributes, threshold value for continuous attributes
        best_threshold = None
        for attr_idx, attribute in enumerate(cur_attributes):
            index_of_attribute = self.attributes.index(attribute)
            if not self.is_continuous_attr(attribute):
                # split cur_data into n-subsets, where n is the number of
                # different values of attribute i. Choose the attribute with
                # the max gain
                values_for_attribute = self.attr_values[attribute]
                subsets = [[] for a in values_for_attribute]  # thống kê các mẫu có thuộc tính chứa giá trị này
                for row in cur_data:
                    for index in range(len(values_for_attribute)):
                        if row[index_of_attribute] == values_for_attribute[index]:  # index ?
                            subsets[index].append(row)
                            break
                e = gain_ratio(cur_data, subsets, self.classes)
                if e > max_ent:
                    max_ent = e
                    splitted = subsets
                    best_attribute = attribute
                    best_threshold = None
            else:
                # sort the data according to the column.Then try all
                # possible adjacent pairs. Choose the one that
                # yields maximum gain
                cur_data.sort(key=lambda x: x[index_of_attribute])
                for j in range(0, len(cur_data) - 1):
                    if cur_data[j][index_of_attribute] != cur_data[j + 1][index_of_attribute]:
                        threshold = (cur_data[j][index_of_attribute] + cur_data[j + 1][
                            index_of_attribute]) / 2  # gia tri trung binh 2 row lien ke
                        less = []  # tap con co gia tri thuoc tinh < threshold
                        greater = []
                        for row in cur_data:
                            if (row[index_of_attribute] > threshold):
                                greater.append(row)
                            else:
                                less.append(row)
                        e = gain_ratio(cur_data, [less, greater], self.classes)  # test do do thong tin khi chia nguong
                        if e > max_ent:
                            splitted = [less, greater]
                            max_ent = e
                            best_attribute = attribute
                            best_threshold = threshold

        return best_attribute, best_threshold, splitted

    # ------------TỈA CÂY------------
    def validate(self, tree, data):
        result = []
        error = 0
        for row in data:
            result.append(self.predict(tree, row))
        for idx, r in enumerate(result):
            if data[idx][-1] != r:
                error += 1

        return error

    # Tính giá trị lỗi sau khi tỉa cây(trước khi thêm nhánh đang xét)
    def get_pessimistic_err_before(self, tree, data):
        error = (self.validate(tree, data)) / len(data)
        
        return error

    # Tính giá trị lỗi trước khi tỉa cây(sau khi thêm nhánh đang xét)
    def get_pessimistic_err_after(self, tree, data, numberOfLeafs):
        error = (self.validate(tree, data) + numberOfLeafs * 0.5) / len(data)

        return error

    def prune_the_tree(self):
        self.pruned_tree = self.tree
        self.prune(self.pruned_tree)
        self.print_tree(self.pruned_tree)

        return self.pruned_tree

    # Tỉa cây
    def prune(self, node):
        if not node.is_leaf:
            for child in node.children:
                self.prune(child)
            after = self.get_pessimistic_err_after(self.pruned_tree, node.subset_data, len(node.children))
            # la node sat nhat voi leaf
            tmp_children = node.children
            tmp_label = node.label
            # print(str(node.is_leaf) + ' ' + tmpLabel + ' ' + str(node._id))
            node.is_leaf = True
            node.children = None
            node.label = node.maj_class
            before = self.get_pessimistic_err_before(self.pruned_tree, node.subset_data)

            # neu khong can tia
            if before > after:
                node.children = tmp_children
                node.is_leaf = False
                node.label = tmp_label

        return
