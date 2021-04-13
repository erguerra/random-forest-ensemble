import copy

from data.BootstrapGenerator import BootstrapGenerator
from dt.DecisionTree import DecisionTree


class RandomForest:
    def __init__(self, d, n, target_column_name):
        self.dataset = d
        self.number_of_trees = n
        self.trees = []
        self.target_column_name = target_column_name

    def create_forest(self):
        bg = BootstrapGenerator(self.dataset)

        for i in range(self.number_of_trees):
            training_set = bg.get_bootstrap()[0]
            dt = DecisionTree(training_set, self.target_column_name)
            dt.should_sample = True
            dt.train_tree()
            self.trees.append(copy.deepcopy(dt))

        return self.trees

    def classify_instance(self, instance):
        if len(self.trees) == 0:
            return 'Empty forest'
        votes = []
        for tree in self.trees:
            votes.append(tree.classify(instance, root_node_tree=tree.root_node))

        return max(set(votes), key=votes.count)


