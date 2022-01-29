import problem
import solver
import analysis
import numpy as np

if __name__ == "__main__":
    seed = 17
    iterations = 1000
    evaluate_every = 10
    dag_factory = problem.DagFactory(5, 10, 5, 10, 50, 50, 100, 200, 300, seed=seed)
    dag = dag_factory.create_dag()
    CCR = problem.calc_ccr(dag)
    print("CCR = " + str(CCR))
    processors = [solver.Processor(20), solver.Processor(15), solver.Processor(10)]
    my_solver = solver.QlHeftSolver(iterations, dag, 1.0, 0.8, processors, seed=seed)
    processors, makespans, speedups, arts, efficiencies = my_solver.solve(evaluate_every=evaluate_every)
    analysis.plot_stats(makespans, speedups, arts, efficiencies, dag_factory, evaluate_every, iterations, CCR)
    print("OK")

