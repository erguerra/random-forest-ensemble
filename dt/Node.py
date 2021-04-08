class Node:
    def __init__(self, d, l):
        self.training_set = d
        self.attribute_list = l
        self.target = 'Defaul Target'
        self.split_attribute = ''
        self.child_tree = ''
