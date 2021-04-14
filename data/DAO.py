import pandas as pd


class DAO:
    def __init__(self, input_file, delimiter, output_file):
        self.inputFile = input_file
        self.delimiter = delimiter
        self.output_file = output_file
        self.dataset = self.read_data()

    def read_data(self):
        return pd.read_csv(self.inputFile, delimiter=self.delimiter)

    def persist_data(self, series):
        series.to_csv(self.output_file, sep=self.delimiter)
