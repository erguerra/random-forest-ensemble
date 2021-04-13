class Node:
    def __init__(self):
        self.level = None
        self.gain = 0
        self.value = None
        self.split_attribute = None
        self.cutting_point = None
        self.leaf_value = None
        self.children = None

    def print_itself(self):
        print(f'level = {self.level}\ngain = {self.gain}\nvalue = {self.value}\nattr = {self.split_attribute}\ncutting_point = {self.cutting_point}\nleaf value = {self.leaf_value}\n')
