import numpy as np


class Dag:
    def __init__(self, T, E_C, W):
        self.T = T  # Tasks, list of lists of ints, each value is a task number, each list is next rank of DAG
        self.E_C = E_C  # Matrix of edges and costs, index is task and value is edge weight, if value is 0 there is no edge
        self.W = W


class DagFactory:
    def __init__(self, min_per_rank, max_per_rank, min_ranks, max_ranks, chance_of_edge, min_edge_cost, max_edge_cost,
                 min_task_cost, max_task_cost, seed):
        self.min_per_rank = min_per_rank  # How wide graf minimaly is
        self.max_per_rank = max_per_rank  # How wide graf maximaly gets
        self.min_ranks = min_ranks  # Minimum number of ranks
        self.max_ranks = max_ranks  # Maximum number of ranks
        self.chance_of_edge = chance_of_edge  # Chance of creating edge between nodes
        self.min_edge_cost = min_edge_cost
        self.max_edge_cost = max_edge_cost
        self.min_task_cost = min_task_cost
        self.max_task_cost = max_task_cost
        self.seed = seed
        np.random.seed(seed)  # set random number generator seed

    def create_dag(self) -> Dag:

        T = []
        ranks = self.min_ranks + np.random.randint(0, high=(self.max_ranks - self.min_ranks) + 1)
        all_nodes = 0
        for i in range(ranks):
            new_nodes = self.min_per_rank + np.random.randint(0, high=(self.max_per_rank - self.min_per_rank) + 1)
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
                        E_C[current_node, lower_node] = np.random.randint(
                            self.min_edge_cost, high=self.max_edge_cost)   # Random value for edge cost

        W = []
        for i in range(all_nodes):
            W.append(np.random.randint(self.min_task_cost, high=self.max_task_cost))  # Random value for task weight

        return Dag(T, E_C, W)


def calc_ccr(dag: Dag):
    mean_c = np.mean(dag.E_C[dag.E_C > 0])
    mean_w = np.mean(dag.W)
    return mean_c/mean_w


