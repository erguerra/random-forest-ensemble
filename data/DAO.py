import pandas as pd


class DAO:
    def __init__(self, inputFile, outputFile):
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.dataset = ""

    def read_data(self):
        self.dataset = pd.read_csv(self.inputFile, delimiter=';')
        return self.dataset
