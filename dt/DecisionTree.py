import copy
import random
from math import sqrt, log

from dt.Node import Node

GREATER_THAN_KEY = "greater_than_"
LESS_OR_EQUAL_THAN_KEY = "less_or_eq_than_"


class DecisionTree:

    def __init__(self, d, target_column_name):
        self.d = d
        self.l = list(self.d.columns)
        self.l.remove(target_column_name)
        self.target_column_name = target_column_name
        self.should_sample = False
        self.root_node = None


    def sample_attributes(self, l):
        num_of_attributes = round(sqrt(len(l)))
        max_index = len(l) - 1
        new_l = []
        while len(new_l) < num_of_attributes:
            random_index = random.randint(0, max_index)
            attribute = l[random_index]
            if attribute not in new_l:
                new_l.append(l[random_index])
        return new_l

    def get_target_column(self, d):
        return d[self.target_column_name]

    def get_most_frequent_class(self, d):
        most_frequent_class = self.get_target_column(d).value_counts().idxmax()
        return most_frequent_class

    def get_classes(self, d):
        class_list = self.get_target_column(d).unique()
        return class_list

    '''
    In order to use this approach, it was necessary to make changes at the wine-recognition.tsv file
    Since the categorical data can also be represented as numbers (int64), all numbers that needs to be 
    considered as continuous attributes must be represented by floating point numbers (float64), hence with a decimal point i.e(1.0). 
    '''

    def split_data(self, d, attribute):
        if str(d[attribute].dtypes) == 'float64':
            return self.split_numerical(d, attribute)
        else:
            return self.split_categorical(d, attribute)

    def split_categorical(self, d, attribute):
        new_data_set_list = d.groupby(attribute)
        data_sets = {}
        for n, g in new_data_set_list:
            data_sets[n] = g
        return data_sets

    def split_numerical(self, d, attribute):
        cutting_point = round(d[attribute].mean(), 3)
        data_sets = {}
        data_sets[GREATER_THAN_KEY + str(cutting_point)] = d[d[attribute] > cutting_point]
        data_sets[LESS_OR_EQUAL_THAN_KEY + str(cutting_point)] = d[d[attribute] <= cutting_point]
        return data_sets

    def entropy(self, d):
        target_column = d[d.columns[-1]]
        summ = 0
        probabilities = target_column.value_counts(True)
        for c, p in probabilities.items():
            log_p = log(p, 2)
            summ -= (p * log_p)
        return summ

    def gain(self, d, attribute):
        info_a = 0
        info_d = self.entropy(d)
        groups = self.split_data(d, attribute)
        for n, g in groups.items():
            info_a += ((g.size / d.size) * self.entropy(g))
        final_gain = info_d - info_a
        return final_gain

    def get_best_attribute(self, d, l):
        attr_to_gain = {}
        for attr in l:
            attr_to_gain[attr] = self.gain(d, attr)
        best_attribute = max(attr_to_gain, key=lambda key: attr_to_gain[key])
        return best_attribute, round(attr_to_gain[best_attribute], 4)

    def train_tree(self):
        d = self.d
        l = self.l
        self.root_node = copy.deepcopy(self.induction_algorithm(d, l))

    def induction_algorithm(self, d, l):
        if self.should_sample:
            sampled_l = self.sample_attributes(l)
        else:
            sampled_l = l
        node = Node()
        present_classes = self.get_classes(d)

        if len(present_classes) == 1:
            node.children = None
            node.leaf_value = present_classes[0]
            return node
        else:
            if len(sampled_l) == 0:
                node.children = None
                node.leaf_value = self.get_most_frequent_class(d)
                return node
            else:
                selected_attribute, gain = self.get_best_attribute(d, sampled_l)
                node.split_attribute = selected_attribute
                node.gain = gain
                if str(d[selected_attribute].dtypes) == 'float64':
                    node.cutting_point = round(d[selected_attribute].mean(), 3)
                sampled_l.remove(selected_attribute)
                node.children = {}
                for k, v in self.split_data(d, selected_attribute).items():
                    new_node = self.induction_algorithm(v, sampled_l)
                    new_node.value = k
                    node.children[k] = new_node

        return node

    def classify(self, instance, root_node_tree):
        if root_node_tree.children is not None:
            value = instance[root_node_tree.split_attribute]
            if value.dtype == 'float64':
                if value > root_node_tree.cutting_point:
                    child_key = GREATER_THAN_KEY + str(root_node_tree.cutting_point)
                else:
                    child_key = LESS_OR_EQUAL_THAN_KEY + str(root_node_tree.cutting_point)
            else:
                child_key = value
            next_node = root_node_tree.children[child_key]
            return self.classify(instance, next_node)
        return root_node_tree.leaf_value

    def print_tree(self, root_node):
        if root_node.children is not None:
            print(f'Attribute {root_node.split_attribute} Gain {root_node.gain}\n')
            for k, v in root_node.children.items():
                if (v.split_attribute is not None):
                    print(f'{root_node.split_attribute} is {k} leads to: {v.split_attribute}')
                else:
                    print(f'{root_node.split_attribute} is {k} leads to leaf: {v.leaf_value}\n')
            for k, v in root_node.children.items():
                self.print_tree(v)
