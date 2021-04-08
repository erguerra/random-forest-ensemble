from data.DAO import DAO
from dt.DecisionTree import DecisionTree


def main():
    dao = DAO('data/benchmark.csv', 'output.csv')
    df = dao.read_data()
    dt = DecisionTree(df, list(df.columns[:df.columns.size-1]))
    dt.decision_tree(dt.d, dt.l)


if __name__ == '__main__':
    main()
