import numpy as np
np.random.seed(1)  # Always use the same seed


class Dag:
    def __init__(self, T, E_C, W):
        self.T = T  # Tasks, list of lists of ints, each value is a task number, each list is next rank of DAG
        self.E_C = E_C  # Matrix of edges and costs, index is task and value is edge weight, if value is 0 there is no edge
        self.W = W


class DagFactory:
    def __init__(self, min_per_rank, max_per_rank, min_ranks, max_ranks, chance_of_edge):
        self.min_per_rank = min_per_rank  # How wide graf minimaly is
        self.max_per_rank = max_per_rank  # How wide graf maximaly gets
        self.min_ranks = min_ranks  # Minimum number of ranks
        self.max_ranks = max_ranks  # Maximum number of ranks
        self.chance_of_edge = chance_of_edge  # Chance of creating edge between nodes

    def create_dag(self):

        T = []
        ranks = self.min_ranks + np.random.randint(0, high=(self.max_ranks - self.min_ranks))
        all_nodes = 0
        for i in range(ranks):
            new_nodes = self.min_per_rank + np.random.randint(0, high=(self.max_per_rank - self.min_per_rank))
            T_rank = []
            for j in range(new_nodes):
                T_rank.append(all_nodes + j)
            all_nodes += new_nodes

            T.append(T_rank)

        E_C = np.zeros((all_nodes, all_nodes))
        for i in range(ranks - 1):
            for j in range(len(T[i])):
                current_node = T[i][j]
                for k in range(len(T[i + 1])):
                    lower_node = T[i + 1][k]
                    if np.random.randint(0, high=100) < self.chance_of_edge:
                        E_C[current_node, lower_node] = np.random.randint(1, high=5)   # Random value for edge cost

        W = []
        for i in range(all_nodes):
            W.append(np.random.randint(10, high=20))  # Random value for task weight

        return Dag(T, E_C, W)




