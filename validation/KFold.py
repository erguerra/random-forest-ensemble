import copy
import pandas as pd
from pandas import DataFrame
from math import floor
from statistics import mean

from random_forest.RandomForest import RandomForest


class KFold:
    def __init__(self, d, k, target_column_name, forest_size=1):
        self.dataset = d
        self.k = k
        self.target_column_name = target_column_name
        self.forest_size = forest_size
        self.folds = []
        self.fold_size = floor((d.index.stop - 1) / k)
        self.temp_df = copy.deepcopy(self.dataset)
        self.possible_classes = self.get_possible_classes()
        self.classes_probabilities = self.get_probabilities(self.dataset)

    def get_probabilities(self, d):
        probabilities = d[self.target_column_name].value_counts(True)
        return probabilities

    def get_possible_classes(self):
        return self.dataset[self.target_column_name].unique()

    def get_fold(self):
        fold = []
        for c in self.possible_classes:
            num_of_instances_c = floor(self.classes_probabilities[c] * self.fold_size)
            while num_of_instances_c > 0:
                sample = self.temp_df.sample(replace=True).squeeze()
                if sample[self.target_column_name] == c:
                    fold.append(sample)
                    self.temp_df.drop(sample.name)
                    num_of_instances_c -= 1
        fold_df = DataFrame(data=fold)

        # Because of the way the algorithm was written we have the instances grouped by their targets
        # in order to mix them up again we execute a sampling of the whole dataframe (frac=1)
        # once the sampling method takes data rows randomly, it's expected that the instances will no longer be grouped
        # by their targets
        return fold_df.sample(frac=1)

    def get_folds_to_test(self, test_fold):
        labels = test_fold[self.target_column_name].values
        test_set = test_fold.drop(columns=self.target_column_name)
        return test_set, labels

    def create_folds(self):
        folds = []
        for i in range(self.k):
            folds.append(self.get_fold())

        self.folds = copy.deepcopy(folds)
        return folds

    def cross_validation(self):
        accuracy_list = []
        for fold_index in range(self.k):
            training_folds = copy.deepcopy(self.folds)
            test_fold = self.folds[fold_index]
            del training_folds[fold_index]
            training_df = pd.concat(training_folds, ignore_index=True)
            forest = RandomForest(training_df, self.forest_size, self.target_column_name)
            forest.create_forest()

            test_fold, expected_labels = self.get_folds_to_test(test_fold)

            generated_labels = []
            for index, instance in test_fold.iterrows():
                classification = forest.classify_instance(instance)
                generated_labels.append(classification)

            hits = 0
            for i in range(len(expected_labels)):
                if expected_labels[i] == generated_labels[i]:
                    hits += 1

            accuracy = round(hits/len(expected_labels), 4)
            accuracy_list.append(accuracy)

        cross_validation_result = round(mean(accuracy_list), 4)

        return cross_validation_result


