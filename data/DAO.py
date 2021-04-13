import pandas as pd


class DAO:
    def __init__(self, inputFile, delimiter):
        self.inputFile = inputFile
        self.delimiter = delimiter
        self.dataset = self.read_data()

    def read_data(self):
        return pd.read_csv(self.inputFile, delimiter=self.delimiter)
