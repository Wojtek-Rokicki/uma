import numpy as np

import problem

np.random.seed(1)


class QlHeftSolver:
    def __init__(self, max_iter, dag: problem.Dag, alfa, discount):
        self.max_iter = max_iter
        self.problem = dag
        self.alfa = alfa
        self.discount = discount

    def __create_ranku_array(self) -> np.ndarray:
        ranku_array = np.zeros(len(self.problem.W))
        for i in range(len(ranku_array)):
            ranku_array[i] = self.__ranku(i)
        return ranku_array

    def __ranku(self, task_index):
        # Check if leaf node
        is_leaf_node = True
        child_tasks = []
        child_index = 0
        for value in self.problem.E_C[task_index]:
            if value != 0:  # it means task contains children task
                is_leaf_node = False
                child_tasks.append(child_index)
            child_index += 1

        # Calculate ranku
        if is_leaf_node:
            return self.problem.W[task_index]
        else:
            child_tasks_ranku = []
            for task in child_tasks:
                child_tasks_ranku.append(self.__ranku(task))

            return self.problem.W[task_index] + max(child_tasks_ranku)

    def __is_new_possible_task(self, task, possible_tasks: list, done_tasks: list) -> bool:
        depends_on = []
        if task not in possible_tasks and task not in done_tasks:
            ec_column = self.problem.E_C[:, task]
            index = 0
            for value in ec_column:
                if value != 0:
                    depends_on.append(index)
                index += 1
        else:
            return False

        possible = True
        for task in depends_on:
            if task not in done_tasks:
                possible = False

        return possible

    def __calculate_q(self, ranku_array, t_current, t_next, Q: np.ndarray, alfa, discount):
        return Q[t_current, t_next] + alfa * (
                    ranku_array[t_current] + discount * max(Q[t_next]) - Q[t_current, t_next])

    def solve(self):
        number_of_nodes = len(self.problem.W)
        Q = np.zeros((number_of_nodes, number_of_nodes))
        ranku_array = self.__create_ranku_array()

        for iter in range(self.max_iter):
            possible_tasks = []
            done_tasks = []
            # check for possible tasks
            for rank in range(len(self.problem.T)):
                for task in self.problem.T[rank]:
                    ec_column = self.problem.E_C[:, task]
                    possible = True
                    for value in ec_column:
                        if value != 0:
                            possible = False
                    if possible:
                        possible_tasks.append(task)

            t_current = np.random.choice(possible_tasks)
            possible_tasks.remove(t_current)
            done_tasks.append(t_current)
            for task_iter in range(len(self.problem.W) - 1):
                # Add to possible tasks all newly unlocked tasks
                for task in range(len(self.problem.W)):
                    if self.__is_new_possible_task(task, possible_tasks, done_tasks):
                        possible_tasks.append(task)

                t_next = np.random.choice(possible_tasks)
                possible_tasks.remove(t_next)
                done_tasks.append(t_next)
                Q[t_current, t_next] = self.__calculate_q(ranku_array, t_current, t_next, Q, 0.2, 0.2)
                t_current = t_next

        # Q array is after learning process
