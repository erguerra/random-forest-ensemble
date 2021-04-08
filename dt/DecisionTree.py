from dt.Node import Node


class DecisionTree:

    def __init__(self, d, l):
        self.d = d
        self.l = l

    def decision_tree(self, d, l):
        node = Node(d, l)
        most_frequent_class = self.is_homogeneous_dataset(d)
        if most_frequent_class != -1:
            node.target = most_frequent_class
            print("Parou por pureza")
            return node
        if len(l) == 0:
            node.target = self.get_most_frequent_class(d)
            print("Parou por falta de atributos")
            return node

        a = l[0]
        l.remove(a)
        print(l)
        grouped_by_attribute = d.groupby(a)
        for name, group in grouped_by_attribute:
            dictionary = {name: self.decision_tree(group, l)}
            print(name + " " + dictionary[name].target)
        node.split_attribute = a

        print("Terminou uma recursão")
        return node

    def is_homogeneous_dataset(self, d):
        class_list = d[d.columns[-1]].unique()
        if len(class_list) == 1:
            return class_list[0]
        return -1

    def get_most_frequent_class(self, d):
        return_value = d[d.columns[-1]].value_counts().idxmax()
        return return_value
