from data.DAO import DAO
from dt.DecisionTree import DecisionTree


def main():
    dao = DAO('data/wine-recognition.tsv', 'output.csv')
    dao.delimiter = '\t'
    df = dao.read_data()
    dt = DecisionTree(df, 'target')
    root_node = dt.induction_algorithm(dt.d, dt.l)

    dt.print_tree(root_node)

    # targets = df['target'].values
    # print(targets)
    # df = df.drop(columns='target')
    #
    # classified = []
    # for i, v in df.iterrows():
    #     classified.append(dt.classify(v, root_node))
    # print(classified)
    #
    # hits = 0
    # for i in range(len(classified)):
    #     if targets[i] == classified[i]:
    #         hits += 1
    # print(hits/len(targets))

    # dao_float = DAO('data/wine-recognition.tsv', 'output.csv')
    # dao_float.delimiter = '\t'
    # df_float = dao_float.read_data()
    #
    # dt = DecisionTree(df_float, 'target')
    # dt.split_numerical_data(df_float, '1')
    # target_column_name = df_float.columns[df_float.columns.size - 1]
    # instances = [df_float.iloc[0], df_float.iloc[1], df_float.iloc[2], df_float.iloc[3], df_float.iloc[4], df_float.iloc[5], df_float.iloc[6]]
    # instances_without_target = []
    # for i in instances:
    #     instances_without_target.append(i.drop(labels=target_column_name))
    #
    # print(f'\n\n\n {dt.l}')

    # for instance in instances_without_target:
    #     print(f'Generated class: {dt.classify(instance, root_node)}\n')

    # dt.print_tree(root_node)


if __name__ == '__main__':
    main()
