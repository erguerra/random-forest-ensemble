import copy
import math

import PIL.ImageQt

from dt.Node import Node

GREATER_THAN_KEY = "greater_than_"
LESS_OR_EQUAL_THAN_KEY = "less_or_eq_than_"

class DecisionTree:

    def __init__(self, d, target_column_name):
        self.d = d
        self.l = list(self.d.columns)
        self.l.remove(target_column_name)

    def get_target_column(self, d):
        return d[d.columns[-1]]

    def get_most_frequent_class(self, d):
        most_frequent_class = self.get_target_column(d).value_counts().idxmax()
        return most_frequent_class

    def get_classes(self, d):
        class_list = self.get_target_column(d).unique()
        return class_list

    def split_data(self, d, attribute):
        new_data_set_list = d.groupby(attribute)
        data_sets = {}
        for n, g in new_data_set_list:
            data_sets[n] = g
        return data_sets

    def split_numerical_data(self, d, attribute):
        cutting_point = round(d[attribute].mean(), 3)
        data_sets = {}
        data_sets[f"greater_than_{cutting_point}"] = d[d[attribute] > cutting_point]
        data_sets[f"less_or_eq_than_{cutting_point}"] = d[d[attribute] <= cutting_point]
        for k, v in data_sets.items():
            print(f'{k}\n\n{v}\n\n')

    def entropy(self, d):
        target_column = d[d.columns[-1]]
        summ = 0
        probabilities = target_column.value_counts(True)
        for c, p in probabilities.items():
            log_p = math.log(p, 2)
            summ -= (p * log_p)
        return summ

    def gain(self, d, attribute):
        info_a = 0
        info_d = self.entropy(d)
        groups = self.split_data(d, attribute)
        for n, g in groups.items():
            info_a += (g.size / d.size) * self.entropy(g)
        final_gain = info_d - info_a
        return final_gain

    def get_best_attribute(self, d, l):
        attr_to_gain = {}
        for attr in l:
            attr_to_gain[attr] = self.gain(d, attr)
        best_attribute = max(attr_to_gain, key=lambda key: attr_to_gain[key])
        return best_attribute

    # def induction_algorithm_numerical(self, d, l):
    def induction_algorithm_cathegorical(self, d, l):
        node = Node()
        present_classes = self.get_classes(d)
        if len(present_classes) == 1:
            node.children = None
            node.leaf_value = present_classes[0]
            return node
        else:
            if len(l) == 0:
                node.children = None
                node.leaf_value = self.get_most_frequent_class(d)
                return node
            else:
                if len(l) > 1:
                    selected_attribute = self.get_best_attribute(d, l)#l.pop(0)
                else:
                    selected_attribute = l[0]
                node.split_attribute = selected_attribute
                l.remove(selected_attribute)
                # d.drop(selected_attribute, axis='columns', inplace=True)
                node.children = {}
                for k, v in self.split_data(d, selected_attribute).items():
                    new_node = self.induction_algorithm(v, l)
                    new_node.value = k
                    node.children[k] = new_node

        return node

    def classify(self, instance, root_node_tree):
        if root_node_tree.children is not None:
            next_node = root_node_tree.children[instance[root_node_tree.split_attribute]]
            return self.classify(instance, next_node)
        return root_node_tree.leaf_value

    def print_tree(self, root_node):
        if root_node.children is not None:
            print(f'Attribute {root_node.split_attribute}\n')
            for k, v in root_node.children.items():
                # print(f'value of {root_node.split_attribute}: {k}\t')
                if (v.split_attribute is not None):
                    print(f'{root_node.split_attribute} equals {k} leads to: {v.split_attribute}\n')
                else:
                    print(f'{root_node.split_attribute} equals {k} leads to leaf: {v.leaf_value}\n')
            for k, v in root_node.children.items():
                self.print_tree(v)

    '''
        We have to calculate the entropy for every partition created
        given an attribute.
        
        So for i to the number of partitions
            calculate sizeOfPartition/sizeOfOriginalDataset  multiplied by the above pseudo code (info gain)
        
        Gain is calculated by subtracting the Info(Attribute) from the entropy of the original dataset
    
        We have to choose the maximum gain
    '''
