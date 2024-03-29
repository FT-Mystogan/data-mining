# from c45 import C45

# c1 = C45("../data/ecoli/ecoli-new.data", "../data/ecoli/ecoli.names")
from c45 import  C45

ratio = 0.6  # thay cái này 0.6 0.7 0.8...

c45 = C45("data/ecoli/" +str(ratio) + "/training/ecoli.data",
          "data/ecoli/" +str(ratio) + "/testing/ecoli.data",
          "data/ecoli/ecoli.names")
# Sử dụng training làm test
# c45 = C45("../data/car/1.0/car.data",
#           "../data/car/1.0/car.data",
#           "../data/car/1.0/car.c45-names")
# c45 = C45("../data/ecoli/1.0/training/ecoli.data",
#           "../data/ecoli/1.0/training/ecoli.data",
#           "../data/ecoli/1.0/ecoli.names")
data, testing_data = c45.get_data()
tree = c45.generate_tree()
c45.print_tree(tree)
c45.test(tree, testing_data)
print('\n ---------pruned-tree--------- \n')
pruned_tree = c45.prune_the_tree()
c45.test(pruned_tree, testing_data)
c45.test_json()


