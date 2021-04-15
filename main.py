import pandas as pd

from data.BootstrapGenerator import BootstrapGenerator
from data.DAO import DAO
from dt.DecisionTree import DecisionTree
from random_forest.RandomForest import RandomForest
from validation.KFold import KFold


def main():
    dao_benchmark = DAO('data/benchmark.csv', ';', 'results/benchmark_results.tsv')
    # dao_numerical = DAO('data/wine-recognition.tsv', '\t', 'results/numerical_results')
    # dao_categorical = DAO('data/house_votes_84.tsv', '\t', 'results/categorical_results')

    # Code to demonstrate the correct implementation of the decision tree
    dt = DecisionTree(dao_benchmark.dataset, 'Joga')
    dt.train_tree()
    dt.print_tree(dt.root_node)
    instance = dao_benchmark.dataset.iloc[1]
    instance.drop(labels='Joga', inplace=True)
    print(instance)
    print(dt.classify(instance=instance, root_node_tree=dt.root_node))


    # Code to execute cross validation

    # forest_sizes = [1, 5, 10, 15, 30, 50, 100]
    #
    #
    # results_categorical = {}
    # for size in forest_sizes:
    #     kfold = KFold(dao_categorical.dataset, 10, target_column_name='target', forest_size=size)
    #     kfold.create_folds()
    #     results_categorical[size] = kfold.cross_validation()
    #
    # results_numerical = {}
    # for size in forest_sizes:
    #     kfold = KFold(dao_numerical.dataset, 10, target_column_name='target', forest_size=size)
    #     kfold.create_folds()
    #     results_numerical[size] = kfold.cross_validation()
    #
    #
    # results_categorical_series = pd.Series(data=results_categorical)
    # results_numerical_series = pd.Series(data=results_numerical)
    #
    # dao_categorical.persist_data(results_categorical_series)
    # dao_numerical.persist_data(results_numerical_series)
    #
    # print('All done!')


if __name__ == '__main__':
    main()
