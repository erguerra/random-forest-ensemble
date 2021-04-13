from data.DAO import DAO
from dt.DecisionTree import DecisionTree


def main():
    dao = DAO('data/house_votes_84.tsv', 'output.csv')
    dao.delimiter = '\t'
    df = dao.read_data()
    # dt = DecisionTree(df, list(df.columns[:df.columns.size-1]))
    # node = dt.decision_tree(dt.d, dt.l)
    # dt = DecisionTree(df)
    # root_node = dt.induction_algorithm(dt.d, dt.l, 0)
    # target_column_name = df.columns[df.columns.size - 1]
    # instances = [df.iloc[0], df.iloc[1], df.iloc[2], df.iloc[3], df.iloc[4], df.iloc[5], df.iloc[6]]
    # instances_without_target = []
    # for i in instances:
    #     # print(f'{i["target"]}\n')
    #     instances_without_target.append(i.drop(labels=target_column_name))
    #
    # print(instances_without_target[0].dtypes)

    dao_float = DAO('data/wine-recognition.tsv', 'output.csv')
    dao_float.delimiter = '\t'
    df_float = dao_float.read_data()

    dt = DecisionTree(df_float, 'target')
    dt.split_numerical_data(df_float, '1')
    target_column_name = df_float.columns[df_float.columns.size - 1]
    instances = [df_float.iloc[0], df_float.iloc[1], df_float.iloc[2], df_float.iloc[3], df_float.iloc[4], df_float.iloc[5], df_float.iloc[6]]
    instances_without_target = []
    for i in instances:
        instances_without_target.append(i.drop(labels=target_column_name))

    print(f'\n\n\n {dt.l}')




    # for instance in instances_without_target:
    #     print(f'Generated class: {dt.classify(instance, root_node)}\n')

    #dt.print_tree(root_node)

if __name__ == '__main__':
    main()
