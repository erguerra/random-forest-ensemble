import random

from pandas import DataFrame

MEAN_BAGGING_TRAINING_SIZE = 63.2
MEAN_BAGGING_TESTING_SIZE = 100 / 3


class BootstrapGenerator:
    def __init__(self, d):
        self.dataset = d

    def get_bootstrap(self):
        test_set = []
        training_set = []

        min_index, max_index = (self.dataset.index.start, self.dataset.index.stop - 1)
        training_set_size = round(MEAN_BAGGING_TRAINING_SIZE / 100 * max_index)
        test_set_size = round(MEAN_BAGGING_TESTING_SIZE / 100 * max_index)
        test_indices = list(self.dataset.index.values)

        # while len(training_set) <= training_set_size:
        #     new_instance_index = random.randint(min_index, max_index)
        #     training_set.append(self.dataset.loc[new_instance_index])
        #     if new_instance_index in test_indices:
        #         test_indices.remove(new_instance_index)
        # training_df = DataFrame(data=training_set)
        training_df = self.dataset.sample(n=training_set_size, replace=True)

        '''
        Even there's more unused indexes in the dataset, the test_set has its size limited at 1/3 of the
        original dataset accordingly to the given example at the page 31 of the ensemble lesson presentation 
        '''

        while len(test_indices) > 0 and len(test_set) < test_set_size:
            test_set.append(self.dataset.loc[test_indices[0]])
            test_indices.pop(0)
        test_df = DataFrame(data=test_set)

        return training_df, test_df
