from concurrent.futures import process
import numpy as np

import problem

np.random.seed(1)

class Processor:
    def __init__(self, speed):
        self.speed = speed
        self.tasks = []
        self.tasks_starts = []

class QlHeftSolver:
    def __init__(self, max_iter, dag: problem.Dag, alfa, discount, processors: list):
        self.max_iter = max_iter
        self.problem = dag
        self.alfa = alfa
        self.discount = discount
        self.processors = processors
        self.mean_processors_speed = np.mean([i.speed for i in processors])

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

    def __get_task_order(self, Q) -> list:
        possible_tasks = []
        task_order = []
        for rank in range(len(self.problem.T)):
            for task in self.problem.T[rank]:
                ec_column = self.problem.E_C[:, task]
                possible = True
                for value in ec_column:
                    if value != 0:
                        possible = False
                if possible:
                    possible_tasks.append(task)

        for iterator in range(len(self.problem.W)):
            max_task = 0
            max_task_q = 0
            for possible_task in possible_tasks:
                row = Q[possible_task]
                max = np.amax(row)
                if max >= max_task_q:
                    max_task_q = max
                    max_task = possible_task
            task_order.append(max_task)
            possible_tasks.remove(max_task)
            for task in range(len(self.problem.W)):
                if self.__is_new_possible_task(task, possible_tasks, task_order):
                    possible_tasks.append(task)
        return task_order

    def __ft(self, task):
        for p in self.processors:
            if task in p.tasks:
                t_id = p.tasks.index(task)
                if len(p.tasks_starts) == 0:
                    return self.problem.W[task]*self.mean_processors_speed/p.speed
                return p.tasks_starts[t_id] + self.problem.W[task]*self.mean_processors_speed/p.speed

    def __at(self, processor):
        if len(processor.tasks) == 0:
            return 0
        return processor.tasks_starts[-1] + self.problem.W[processor.tasks[-1]]*self.mean_processors_speed/processor.speed

    def __est(self, task, processor):
        avaliable_predecessors = self.problem.E_C[:, task]
        predecessors = []
        for i in range(len(avaliable_predecessors)):
            if(avaliable_predecessors[i] != 0):
                predecessors.append(i)

        # Choose the max finish time with communication cost
        predecessors_fts = []
        for i in predecessors:
            predecessors_fts.append(self.__ft(i) + self.problem.E_C[i, task]) # E_c is also a communication cost
        
        if len(predecessors_fts) == 0:
            return self.__at(processor)
        return max(max(predecessors_fts), self.__at(processor))

    def __eft(self, task):
        eft_list=[]
        for p in self.processors:
            speed_on_proc = self.problem.W[task] * self.mean_processors_speed / p.speed
            eft_list.append(speed_on_proc + self.__est(task, p))
        return eft_list
    
    def __allocate_tasks_to_processors(self, tasks):
        for task in tasks:
            efts = self.__eft(task)
            eft_min_id = efts.index(min(efts))
            processor = self.processors[eft_min_id]
            start_time = efts[eft_min_id] - self.problem.W[task] * self.mean_processors_speed / processor.speed
            processor.tasks.append(task)
            processor.tasks_starts.append(start_time)

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

            # Current should be chosen with e greedy strategy
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
        # Create task order
        task_order = self.__get_task_order(Q)
        self.__allocate_tasks_to_processors(task_order)
        

        print("OK")



