import numpy as np
import copy

import problem
import solver
import analysis


seed = 17
iterations = 2000
evaluate_every = 10

dag_factory = problem.DagFactory(5, 8, 5, 8, 30, 50, 100, 200, 300, seed=seed)
#dag_factory = problem.DagFactory(4, 4, 4, 4, 30, 50, 100, 200, 300, seed=seed)
param_experiments_dag = dag_factory.create_dag()
param_experiments_processors = [solver.Processor(20), solver.Processor(15), solver.Processor(10)]

# Use this parameters on parameters test whenever changing others
param_tests_alfa = 0.5
param_tests_discount = 0.8
param_epsilon_start = 1.0
param_epsilon_min = 0.2

# Parameters chosen after param experiments for different dag experiments
deg_tests_epsilon_start = 1.0
dag_tests_epsilon_min = 0.2
dag_tests_alfa = 0.8
dag_tests_discount = 0.4


def perform_alfa_experiments():
    dag = param_experiments_dag
    for alfa in np.arange(1.0, -0.1, -0.1):
        alfa = float(format(alfa, '.2f'))
        processors = copy.deepcopy(param_experiments_processors)
        my_solver = solver.QlHeftSolver(iterations, dag, alfa, param_tests_discount, processors,
                                        epsilon_min=param_epsilon_min, epsilon_start=param_epsilon_start, seed=seed)
        result, makespans, speedups, arts, efficiencies = my_solver.solve(evaluate_every=evaluate_every)
        alfa_str = "{:.1f}".format(alfa)
        analysis.plot_stats(makespans, speedups, arts, efficiencies, dag_factory, evaluate_every, "szybkosc_nauczania",
                            f"alfa{alfa_str}")


def perform_discount_experiments():
    dag = param_experiments_dag
    for discount in np.arange(1.0, -0.1, -0.1):
        discount = float(format(discount, '.2f'))
        processors = copy.deepcopy(param_experiments_processors)
        my_solver = solver.QlHeftSolver(iterations, dag, param_tests_alfa, discount, processors,
                                        epsilon_min=param_epsilon_min, epsilon_start=param_epsilon_start, seed=seed)
        result, makespans, speedups, arts, efficiencies = my_solver.solve(evaluate_every=evaluate_every)
        discount_str = "{:.1f}".format(discount)
        analysis.plot_stats(makespans, speedups, arts, efficiencies, dag_factory, evaluate_every,
                            "wspolczynnik_zmniejszenia", f"discount{discount_str}")


def perform_epsilon_experiments():
    dag = param_experiments_dag
    for epsilon_min in np.arange(1.0, -0.1, -0.1):
        epsilon_min = float(format(epsilon_min, '.2f'))
        processors = copy.deepcopy(param_experiments_processors)
        my_solver = solver.QlHeftSolver(iterations, dag, param_tests_alfa, param_tests_discount, processors,
                                        epsilon_min=epsilon_min, epsilon_start=param_epsilon_start, seed=seed)
        result, makespans, speedups, arts, efficiencies = my_solver.solve(evaluate_every=evaluate_every)
        epsilon_min = "{:.1f}".format(epsilon_min)
        analysis.plot_stats(makespans, speedups, arts, efficiencies, dag_factory, evaluate_every,
                            "epsilon", f"epsilon_min{epsilon_min}")


def perform_proc_cnt_tests():
    procs2 = [solver.Processor(20), solver.Processor(15)]
    procs3 = [solver.Processor(20), solver.Processor(17), solver.Processor(15)]
    procs4 = [solver.Processor(20), solver.Processor(19), solver.Processor(17),
              solver.Processor(15)]
    procs5 = [solver.Processor(20), solver.Processor(19), solver.Processor(17),
              solver.Processor(16), solver.Processor(15)]
    experiment_procs = [procs2, procs3, procs4, procs5]

    dag = param_experiments_dag
    for procs in experiment_procs:
        my_solver = solver.QlHeftSolver(iterations, dag, dag_tests_alfa, dag_tests_discount, procs,
                                        epsilon_min=dag_tests_epsilon_min, epsilon_start=deg_tests_epsilon_start,
                                        seed=seed)

        result, makespans, speedups, arts, efficiencies = my_solver.solve(evaluate_every=evaluate_every)
        procs_cnt = len(procs)
        analysis.plot_stats(makespans, speedups, arts, efficiencies, dag_factory, evaluate_every,
                            "procs_cnt", f"procs_cnt{procs_cnt}")


def perform_dag_edge_tests():
    for edge_chance in np.arange(100.0, -10, -10):
        factory = problem.DagFactory(12, 12, 7, 7, edge_chance, 50, 100, 10, 300, seed=seed)
        dag = factory.create_dag()
        processors = copy.deepcopy(param_experiments_processors)
        my_solver = solver.QlHeftSolver(iterations, dag, dag_tests_alfa, dag_tests_discount, processors,
                                        epsilon_min=dag_tests_epsilon_min, epsilon_start=dag_tests_epsilon_min,
                                        seed=seed)
        result, makespans, speedups, arts, efficiencies = my_solver.solve(evaluate_every=evaluate_every)
        analysis.plot_stats(makespans, speedups, arts, efficiencies, dag_factory, evaluate_every,
                            "prawdopodobienstwo_edge", f"edge_chance{edge_chance}")


def perform_dag_task_cnt_tests():
    for task_in_rank in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
        factory = problem.DagFactory(task_in_rank, task_in_rank, 7, 7, 30, 50, 100, 200, 300, seed=seed)
        dag = factory.create_dag()
        processors = copy.deepcopy(param_experiments_processors)
        my_solver = solver.QlHeftSolver(iterations, dag, dag_tests_alfa, dag_tests_discount, processors,
                                        epsilon_min=dag_tests_epsilon_min, epsilon_start=dag_tests_epsilon_min,
                                        seed=seed)
        result, makespans, speedups, arts, efficiencies = my_solver.solve(evaluate_every=evaluate_every)
        analysis.plot_stats(makespans, speedups, arts, efficiencies, dag_factory, evaluate_every,
                            "ilosc_zadan", f"tasks_in_rank{task_in_rank}")




